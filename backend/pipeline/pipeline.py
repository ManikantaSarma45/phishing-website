# from preprocessing import Preprocessing
# from features import FeatureExtraction
# from train import TrainModel
# from predict import Predict
from src import preprocess, features, predict

class Pipeline:
    def set_url(self, url: str):
        self.url = url

    def create_pipeline(self):
        # print(f"\n{self.url}")
        pp = preprocess.Preprocessing()
        fe = features.FeatureExtraction()
        # t = TrainModel()
        p = predict.Predict()
        preprocessed_url = pp.preprocess(self.url)
        # print(url)
        features = fe.extract_features(preprocessed_url)
        # print(features)
        # t.train_model()
        prediction = p.predict(features)
        return prediction
        # print(prediction)
