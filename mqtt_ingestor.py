import paho.mqtt.client as mqtt
import json
import logging
import requests

# MQTT Config
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "/iot/data"

# Backend API URL
BACKEND_URL = "http://localhost:5000/api/ingest"

# Setup logging
logging.basicConfig(level=logging.INFO)

# MQTT callback functions
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        logging.info("✅ Connected to MQTT Broker!")
        client.subscribe(MQTT_TOPIC)
    else:
        logging.error(f"❌ Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        data = json.loads(payload)

        logging.info(f"📩 MQTT Data Received: {data}")

        features = [
            data.get("packet_size"),
            data.get("request_rate"),
            data.get("source_ip_entropy"),
            data.get("destination_port"),
            data.get("protocol"),
            data.get("payload_size")
        ]

        ingest_payload = {
            "device_id": data.get("device_id", "unknown"),
            "features": features,
            "raw_data": json.dumps(data)  # 👍 Store raw original data
        }

        response = requests.post(BACKEND_URL, json=ingest_payload, timeout=5)
        if response.status_code == 200:
            result = response.json()
            logging.info(f"✅ Data ingested: {result}")
        else:
            logging.warning(f"⚠️ Ingest failed: {response.text}")

    except Exception as e:
        logging.error(f"❌ Error processing message: {e}")

# Start MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()
except Exception as e:
    logging.error(f"❌ Could not connect to MQTT broker: {e}")
