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
    score = model.predict_proba(X_scaled)[0][1]
    if score < 0.5:
        score = (1 - score * 2) * 100
    else:
        score = ((score - 0.5) * 2) * 100

    logger.info(f"Predicted: {'Legit' if prediction == 0 else 'Phishing'}")
    logger.info(f"Confidence Score: {score: .2f}%")
    return prediction, score
