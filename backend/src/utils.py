import logging
from pathlib import Path
import os
import pickle

ROOT_DIR = Path(__file__).resolve().parents[1]
LOGS_DIR = ROOT_DIR / "logs"
MODEL_PATH = os.path.join("backend", "models")
DATA_PATH = os.path.join("backend", "data")

LOGS_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOGS_DIR / "app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def save_model(model):
    with open(f"{MODEL_PATH}/model_v1.pkl", "wb") as f:
        pickle.dump(model, f)


def load_model():
    with open(f"{MODEL_PATH}/model_v1.pkl", "rb") as f:
        return pickle.load(f)


def save_scaler(model):
    with open(f"{MODEL_PATH}/scaler_v1.pkl", "wb") as f:
        pickle.dump(model, f)


def load_scaler():
    with open(f"{MODEL_PATH}/scaler_v1.pkl", "rb") as f:
        return pickle.load(f)
