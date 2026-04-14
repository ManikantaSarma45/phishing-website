from backend.src.features import FeatureExtraction
from backend.src.preprocess import preprocess
from backend.src.utils import load_model, load_scaler, logger


def predict_url(url: str):
    model = load_model()
    scaler = load_scaler()

    url = preprocess(url)
    extractor = FeatureExtraction()
    features = extractor.extract_features(url)
    # print(features)
    if features is None:
        return -1

    X_scaled = scaler.transform(features)
    logger.info(f"Scaled Features:\n{X_scaled}")
    # features = features[model.feature_names_in_]
    prediction = model.predict(X_scaled)[0]

    logger.info(f"Predicted: {'Legit' if prediction == 0 else 'Phishing'}")
    return prediction
