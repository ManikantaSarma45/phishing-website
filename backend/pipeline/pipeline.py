# from preprocessing import Preprocessing
# from features import FeatureExtraction
# from train import TrainModel
# from predict import Predict
from backend.src import predict, evaluate, train
from backend.src.utils import logger


class Pipeline:
    def set_url(self, url: str):
        self.url = url

    def create_pipeline(self):
        logger.info(f"Sample URL: {self.url}")
        t = train.TrainModel()
        e = evaluate.Evaluate()
        p = predict.Predict()

        # url_features = fe.extract_features(self.url)
        # print(url_features)
        t.train_model()
        e.evaluate_model()
        prediction = p.predict(self.url)
        return prediction
        # print(prediction)


if __name__ == "__main__":
    pl = Pipeline()
    pl.set_url(url="www.google.com")
    pl.create_pipeline()
