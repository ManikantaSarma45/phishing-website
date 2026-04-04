import pickle
import numpy as np
import os
from backend.src.features import FeatureExtraction

MODEL_PATH = os.path.join("backend", "models", "model_v1.pkl")
SCALER_PATH = os.path.join("backend", "models", "scaler_v1.pkl")


class Predict:
    def __init__(self):
        with open(MODEL_PATH, "rb") as f:
            self.model = pickle.load(f)

        with open(SCALER_PATH, "rb") as f:
            self.scaler = pickle.load(f)

    def predict(self, url: str):
        extractor = FeatureExtraction()
        features = extractor.extract_features(url)
        print(features)
        if features is None:
            return -1

        features = np.array(features).reshape(1, -1)
        X_scaled = self.scaler.transform(features)
        prediction = self.model.predict(X_scaled)[0]

        return prediction
