import pandas as pd
from backend.src.utils import DATA_PATH
from tranco import Tranco


def load_model_training_dataset():
    return pd.read_csv(f"{DATA_PATH}/final_merged_dataset.csv")


def load_url_shorteners() -> set[str]:
    return set(pd.read_csv(f"{DATA_PATH}/url_shorteners.csv").url)


def load_hosting_websites() -> set[str]:
    return set(pd.read_csv(f"{DATA_PATH}/hosting_websites.csv").domain)


def load_tranco_websites() -> set[str]:
    return set(Tranco(cache=True, cache_dir=".tranco").list().top(1000000))
