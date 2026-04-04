import pickle
import numpy as np
import os
from backend.src.preprocess import Preprocessing
from backend.src.features import FeatureExtraction

MODEL_PATH = os.path.join("backend", "models")
DATA_PATH = os.path.join("backend", "data")


class Predict:
    def __init__(self):
        with open(f"{MODEL_PATH}/model_v1.pkl", "rb") as f:
            self.model = pickle.load(f)

        with open(f"{MODEL_PATH}/scaler_v1.pkl", "rb") as f:
            self.scaler = pickle.load(f)

    def predict(self, url: str):
        preprocess = Preprocessing()
        extractor = FeatureExtraction()
        url = preprocess.preprocess(url)
        features = extractor.extract_features(url)
        # print(features)
        if features is None:
            return -1

        features = np.array(features).reshape(1, -1)
        X_scaled = self.scaler.transform(features)
        prediction = self.model.predict(X_scaled)[0]

        return prediction
