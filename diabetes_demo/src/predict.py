import os

import joblib
import numpy as np

from src.data_preparation import FEATURE_COLUMNS

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")


def load_model():
    model = joblib.load(os.path.join(MODELS_DIR, "model.joblib"))
    scaler = joblib.load(os.path.join(MODELS_DIR, "scaler.joblib"))
    return model, scaler


def predict(input_dict: dict) -> dict:
    model, scaler = load_model()

    features = np.array([[input_dict[col] for col in FEATURE_COLUMNS]])
    features_scaled = scaler.transform(features)

    prediction = model.predict(features_scaled)[0]
    probability = model.predict_proba(features_scaled)[0]

    return {
        "prediction": int(prediction),
        "label": "Có nguy cơ tiểu đường" if prediction == 1 else "Không có nguy cơ tiểu đường",
        "probability_no_diabetes": float(probability[0]),
        "probability_diabetes": float(probability[1]),
    }
