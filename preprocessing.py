import pandas as pd
import numpy as np
import joblib

def preprocess_input(data: dict) -> np.ndarray:
    """
    Preprocess incoming IoT cybersecurity threat data to be compatible with the trained model.

    Args:
        data (dict): A dictionary representing the incoming IoT threat data.

    Returns:
        np.ndarray: Processed features ready for model prediction.
    """
    df = pd.DataFrame([data])

    # Convert numeric fields
    numeric_fields = ["packet_size", "request_rate", "source_ip_entropy", "destination_port", "payload_size"]
    for field in numeric_fields:
        df[field] = pd.to_numeric(df.get(field, 0), errors="coerce")
        df[field] = df[field].fillna(df[field].mean())

    # Encode protocol using the saved label encoder
    try:
        protocol_encoder = joblib.load('label_encoder_protocol.joblib')
        df["protocol"] = protocol_encoder.transform(df.get("protocol").fillna('Unknown'))
    except Exception as e:
        print(f"Error encoding protocol: {e}")
        df["protocol"] = -1

    # Select the exact features expected by the model
    features = df[[
        "packet_size",
        "request_rate",
        "source_ip_entropy",
        "destination_port",
        "protocol",
        "payload_size"
    ]]

    return features.values  # shape: (1, 6)
