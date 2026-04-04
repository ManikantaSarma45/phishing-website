import pandas as pd
import pickle
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from backend.src.utils import logger
import os

MODEL_PATH = os.path.join("backend", "models")
DATA_PATH = os.path.join("backend", "data")


class Evaluate:
    def __init__(self):
        self.df = pd.read_csv(f"{DATA_PATH}/final_merged_dataset.csv")
        self.df = self.df.drop_duplicates()

    def data_preprocess(self):
        if "url" in self.df.columns:
            self.df = self.df.drop(columns=["url"])

        if "https" in self.df.columns:
            self.df = self.df.drop(columns=["https"])

        # Split
        X = self.df.iloc[:, :-1]
        y = self.df.iloc[:, -1]

        # Load model + scaler
        with open(f"{MODEL_PATH}/scaler_v1.pkl", "rb") as f:
            self.scaler = pickle.load(f)

        with open(f"{MODEL_PATH}/model_v1.pkl", "rb") as f:
            self.model = pickle.load(f)

        # Scale
        X_scaled = self.scaler.transform(X)

        # Split
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=64, shuffle=True
        )

    # Predict
    def evaluate_model(self):
        self.data_preprocess()
        y_pred = self.model.predict(self.X_test)

        # Metrics
        logger.info(f"Accuracy:  {accuracy_score(self.y_test, y_pred)}")
        logger.info(f"\nConfusion Matrix:\n {confusion_matrix(self.y_test, y_pred)}")
        logger.info(
            f"\nClassification Report:\n {classification_report(self.y_test, y_pred)}"
        )
