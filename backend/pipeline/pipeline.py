from backend.src import predict, evaluate, train
from backend.src.utils import logger


class Pipeline:
    def set_url(self, url: str):
        self.url = url

    def create_pipeline(self):
        logger.info(f"Sample URL: {self.url}")
        e = evaluate.Evaluate()

        # url_features = fe.extract_features(self.url)
        # print(url_features)
        train.train_model()
        e.evaluate_model()
        prediction = predict.predict_url(self.url)
        return prediction


if __name__ == "__main__":
    pl = Pipeline()
    pl.set_url(url="www.google.com")
    pl.create_pipeline()
