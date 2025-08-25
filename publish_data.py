import paho.mqtt.client as mqtt
import json
import time
import random

# MQTT Config
BROKER_ADDRESS = "localhost"
PORT = 1883
TOPIC = "/iot/data"
USERNAME = "your_username"
PASSWORD = "your_password"

# Devices and protocols
DEVICE_IDS = ["device_001", "device_002", "device_003"]
PROTOCOLS = ["TCP", "UDP", "ICMP"]

# Setup MQTT client
client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)
client.connect(BROKER_ADDRESS, PORT, 60)

# Simulate realistic attack patterns
def generate_sample(label):
    base = {
        "device_id": random.choice(DEVICE_IDS),
        "protocol": random.choice(PROTOCOLS),
        "destination_port": random.choice([80, 443, 8080, 53])
    }

    if label == "Normal":
        return {
            **base,
            "packet_size": random.randint(100, 400),
            "request_rate": round(random.uniform(0.1, 1.0), 2),
            "source_ip_entropy": round(random.uniform(0.1, 1.5), 2),
            "payload_size": random.randint(100, 500),
            "label": "Normal"
        }

    elif label == "Unauthorized Access":
        return {
            **base,
            "packet_size": random.randint(100, 700),
            "request_rate": round(random.uniform(1.0, 3.0), 2),
            "source_ip_entropy": round(random.uniform(3.0, 5.0), 2),
            "destination_port": random.choice([22, 23, 3389]),  # suspicious ports
            "payload_size": random.randint(200, 800),
            "label": "Unauthorized Access"
        }

    elif label == "DoS":
        return {
            **base,
            "packet_size": random.randint(500, 1200),
            "request_rate": round(random.uniform(10.0, 50.0), 2),
            "source_ip_entropy": round(random.uniform(0.5, 1.0), 2),
            "payload_size": random.randint(800, 1500),
            "label": "DoS"
        }

    elif label == "DDoS":
        return {
            **base,
            "packet_size": random.randint(800, 1500),
            "request_rate": round(random.uniform(20.0, 100.0), 2),
            "source_ip_entropy": round(random.uniform(3.0, 5.0), 2),  # many sources
            "payload_size": random.randint(1000, 2000),
            "label": "DDoS"
        }

# Publish simulated data
def publish_data():
    labels = ["Normal", "Unauthorized Access", "DoS", "DDoS"]
    for _ in range(20):  # Publish 20 samples
        label = random.choice(labels)
        data = generate_sample(label)
        payload = json.dumps(data)
        client.publish(TOPIC, payload)
        print(f"📤 Published: {payload}")
        time.sleep(0.5)

if __name__ == "__main__":
    publish_data()
    client.disconnect()
