import pandas as pd
import pickle
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split

df = pd.read_csv("final_merged_dataset.csv")
df = df.drop_duplicates()

if "url" in df.columns:
    df = df.drop(columns=["url", "https"])

# Split
X = df.iloc[:, :-1]
y = df.iloc[:, -1]

# Load model + scaler
with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# Scale
X_scaled = scaler.transform(X)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=64
)

# Predict
y_pred = model.predict(X_test)

# Metrics
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))