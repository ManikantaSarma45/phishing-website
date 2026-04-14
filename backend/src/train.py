from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

from backend.src.utils import save_model, save_scaler
from backend.src.data_loader import load_model_training_dataset


def train_model():
    df = load_model_training_dataset()
    df = df.drop_duplicates()
    X_train = None
    X_test = None
    y_train = None
    y_test = None

    if "url" in df.columns:
        df = df.drop(columns=["url"])
    if "https" in df.columns:
        df = df.drop(columns=["https"])
    if "tranco_indexed" in df.columns:
        df = df.drop(columns=["tranco_indexed"])

    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=64, shuffle=True
    )

    model = XGBClassifier(
    max_depth=12,
    # learning_rate=0.1,
    n_estimators=500,
    # reg_alpha=0.1,
    # reg_lambda=10
)   
    # X_train = X_train[model.feature_names_in_]
    model.fit(X_train, y_train)
    # model.fit(X_train, y_train)

    save_model(model)
    save_scaler(scaler)
