import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier
import os

DATA_PATH = os.path.join("backend", "data")
MODEL_PATH = os.path.join("backend", "models")


class TrainModel:
    def __init__(self):
        self.df = pd.read_csv(f"{DATA_PATH}/final_merged_dataset.csv")
        self.df = self.df.drop_duplicates()
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

        if "url" in self.df.columns:
            self.df = self.df.drop(columns=["url"])
        if "https" in self.df.columns:
            self.df = self.df.drop(columns=["https"])

    def data_preprocess(self):
        X = self.df.iloc[:, :-1]
        y = self.df.iloc[:, -1]

        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=64, shuffle=True
        )

    def train_model(self):
        self.data_preprocess()
        self.model = XGBClassifier(max_depth=12)
        self.model.fit(self.X_train, self.y_train)

        with open(f"{MODEL_PATH}/model_v1.pkl", "wb") as f:
            pickle.dump(self.model, f)

        with open(f"{MODEL_PATH}/scaler_v1.pkl", "wb") as f:
            pickle.dump(self.scaler, f)
