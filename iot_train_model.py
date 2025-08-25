import pandas as pd
import numpy as np
import random
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

# ----------------------
# STEP 1: GENERATE SYNTHETIC DATASET
# ----------------------

def generate_data(label, n):
    data = {
        'packet_size': [],
        'request_rate': [],
        'source_ip_entropy': [],
        'destination_port': [],
        'protocol': [],
        'payload_size': [],
        'label': []
    }

    for _ in range(n):
        if label == 'Normal':
            data['packet_size'].append(np.random.normal(200, 30))
            data['request_rate'].append(np.random.normal(5, 1))
            data['source_ip_entropy'].append(np.random.normal(4.5, 0.5))
            data['destination_port'].append(random.choice([80, 443, 5683]))
            data['protocol'].append(random.choice(['TCP', 'UDP']))
            data['payload_size'].append(np.random.normal(120, 20))
        elif label == 'Unauthorized Access':
            data['packet_size'].append(np.random.normal(250, 40))
            data['request_rate'].append(np.random.normal(7, 1.5))
            data['source_ip_entropy'].append(np.random.normal(6, 0.7))
            data['destination_port'].append(random.choice([22, 8080]))
            data['protocol'].append(random.choice(['UDP', 'ICMP']))
            data['payload_size'].append(np.random.normal(200, 25))
        elif label == 'DoS':
            data['packet_size'].append(np.random.normal(500, 100))
            data['request_rate'].append(np.random.normal(50, 10))
            data['source_ip_entropy'].append(np.random.normal(2.5, 0.5))
            data['destination_port'].append(random.choice([80, 5683]))
            data['protocol'].append(random.choice(['TCP', 'ICMP']))
            data['payload_size'].append(np.random.normal(100, 50))
        elif label == 'DDoS':
            data['packet_size'].append(np.random.normal(600, 120))
            data['request_rate'].append(np.random.normal(100, 20))
            data['source_ip_entropy'].append(np.random.normal(1.5, 0.3))
            data['destination_port'].append(random.choice([443, 5683]))
            data['protocol'].append(random.choice(['TCP', 'UDP', 'ICMP']))
            data['payload_size'].append(np.random.normal(150, 30))

        data['label'].append(label)

    return pd.DataFrame(data)

print("🔄 Generating synthetic IoT threat dataset...")
n_samples = 500
df = pd.concat([
    generate_data('Normal', n_samples),
    generate_data('Unauthorized Access', n_samples),
    generate_data('DoS', n_samples),
    generate_data('DDoS', n_samples)
])

df = df.sample(frac=1).reset_index(drop=True)
df.to_csv("iot_threat_dataset.csv", index=False)
print("✅ Dataset saved as iot_threat_dataset.csv")

# ----------------------
# STEP 2: TRAIN MODEL
# ----------------------

print("\n🔄 Training model...")

X = df.drop("label", axis=1)
y = df["label"]

# Encode protocol column
protocol_encoder = LabelEncoder()
X['protocol'] = protocol_encoder.fit_transform(X['protocol'])

# ✅ Save protocol encoder
joblib.dump(protocol_encoder, "label_encoder_protocol.joblib")
print("✅ Saved: label_encoder_protocol.joblib")

# Encode label column
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# ✅ Save label encoder
joblib.dump(label_encoder, "label_encoder.joblib")
print("✅ Saved: label_encoder.joblib")

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Train
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Predict and evaluate
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"✅ Model Accuracy: {accuracy:.4f}")
print("📊 Classification Report:")
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

# ----------------------
# STEP 3: SAVE MODEL
# ----------------------

joblib.dump(clf, "model_iot_real.joblib")
print("✅ Saved: model_iot_real.joblib")

# ----------------------
# STEP 4: CLEANED DATASET
# ----------------------

df_cleaned = df.copy()
df_cleaned.to_csv("iot_threat_cleaned.csv", index=False)
print("✅ Saved: iot_threat_cleaned.csv")
