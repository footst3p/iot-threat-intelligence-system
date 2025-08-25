from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import joblib
import numpy as np
import sqlite3
import logging
from datetime import datetime
from preprocessing import preprocess_input
import paho.mqtt.publish as publish

# -------------------------------
# Initialize Flask and SocketIO
# -------------------------------
app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Replace in production
CORS(app, supports_credentials=True)

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# -------------------------------
# Load ML model and encoders
# -------------------------------
model = joblib.load("model_iot_real.joblib")
label_encoder = joblib.load("label_encoder.joblib")
protocol_encoder = joblib.load("label_encoder_protocol.joblib")

# MQTT config
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "/iot/predictions"

# Logging
logging.basicConfig(level=logging.INFO)

# -------------------------------
# Initialize Database
# -------------------------------
def init_db():
    conn = sqlite3.connect('iot_threat.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )''')
    cursor.execute("SELECT * FROM users WHERE username = ?", ('admin',))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('admin', 'admin123'))

    cursor.execute('''CREATE TABLE IF NOT EXISTS devices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id TEXT UNIQUE NOT NULL
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        device_id TEXT,
        label TEXT,
        confidence REAL
    )''')

    conn.commit()
    conn.close()

init_db()

# -------------------------------
# Routes
# -------------------------------

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the IoT Threat Intelligence System!"})

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    conn = sqlite3.connect("iot_threat.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        session["user"] = username
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Invalid credentials"}), 401

# 🚀 NEW: Signup Route
@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    conn = sqlite3.connect("iot_threat.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        session["user"] = username  # Auto-login after signup
        return jsonify({"message": "Signup successful"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"message": "Username already exists"}), 400
    finally:
        conn.close()

# 🚀 NEW: Logout Route
@app.route("/api/logout", methods=["POST"])
def logout():
    if "user" in session:
        session.pop("user")
        return jsonify({"message": "Logout successful"}), 200
    return jsonify({"message": "No user logged in"}), 400

@app.route("/api/logs", methods=["GET"])
def get_logs():
    if "user" not in session:
        return jsonify({"message": "Unauthorized"}), 401

    conn = sqlite3.connect("iot_threat.db")
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, device_id, label, confidence FROM predictions ORDER BY timestamp DESC LIMIT 100")
    rows = cursor.fetchall()
    conn.close()

    logs = []
    for row in rows:
        logs.append({
            "timestamp": row[0],
            "device_id": row[1],
            "prediction_label": row[2],
            "confidence": row[3],
            "status": "Anomalous" if row[2] != "Normal" else "Normal",
            "packet_rate": np.random.randint(50, 300)  # Placeholder
        })
    return jsonify(logs)

@app.route("/api/devices", methods=["GET"])
def get_devices():
    if "user" not in session:
        return jsonify({"message": "Unauthorized"}), 401

    conn = sqlite3.connect("iot_threat.db")
    cursor = conn.cursor()
    cursor.execute("SELECT device_id FROM devices")
    rows = cursor.fetchall()
    conn.close()

    return jsonify([{"device_id": r[0]} for r in rows])

@app.route("/api/devices", methods=["POST"])
def add_device():
    if "user" not in session:
        return jsonify({"message": "Unauthorized"}), 401

    data = request.json
    device_id = data.get("device_id")

    if not device_id:
        return jsonify({"error": "Missing device_id"}), 400

    try:
        conn = sqlite3.connect("iot_threat.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO devices (device_id) VALUES (?)", (device_id,))
        conn.commit()
        conn.close()
        return jsonify({"message": "Device added"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"message": "Device already exists"}), 400

@app.route("/api/devices/<device_id>", methods=["DELETE"])
def delete_device(device_id):
    if "user" not in session:
        return jsonify({"message": "Unauthorized"}), 401

    conn = sqlite3.connect("iot_threat.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM devices WHERE device_id = ?", (device_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Device removed"}), 200

@app.route("/api/ingest", methods=["POST"])
def ingest_data():
    try:
        data = request.json
        logging.info(f"📥 Incoming data: {data}")

        if "features" not in data:
            return jsonify({"error": "Missing 'features' field"}), 400

        features = data["features"]

        try:
            protocol_index = 4
            protocol_str = features[protocol_index]
            encoded_protocol = protocol_encoder.transform([protocol_str])[0]
            features[protocol_index] = encoded_protocol
        except Exception as e:
            return jsonify({"error": f"Invalid protocol: {protocol_str}. Error: {e}"}), 400

        features_np = np.array(features).reshape(1, -1)
        prediction = model.predict(features_np)[0]
        label = label_encoder.inverse_transform([prediction])[0]

        proba = model.predict_proba(features_np)[0]
        confidence = float(np.max(proba))

        conn = sqlite3.connect("iot_threat.db")
        cursor = conn.cursor()
        timestamp = datetime.utcnow().isoformat()
        cursor.execute("INSERT INTO predictions (timestamp, device_id, label, confidence) VALUES (?, ?, ?, ?)",
                       (timestamp, data.get("device_id", "unknown"), label, confidence))
        conn.commit()
        conn.close()

        mqtt_payload = {
            "device_id": data.get("device_id", "unknown"),
            "label": label,
            "confidence": confidence,
            "timestamp": timestamp
        }
        
        # Publish via MQTT
        publish.single(MQTT_TOPIC, payload=str(mqtt_payload), hostname=MQTT_BROKER, port=MQTT_PORT)

        # Emit event to connected Socket.IO clients
        socketio.emit('new_prediction', mqtt_payload)

        logging.info(f"✅ Prediction published and emitted: {mqtt_payload}")

        return jsonify({"label": label, "confidence": confidence}), 200

    except Exception as e:
        logging.error(f"❌ Server error: {e}")
        return jsonify({"error": str(e)}), 500

# -------------------------------
# Main Runner
# -------------------------------
if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
