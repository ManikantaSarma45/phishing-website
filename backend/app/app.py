from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.schema import URLInput
from backend.src.predict import predict_url
from backend.src.utils import logger

# create app
app = FastAPI()

# CORS middleware (important for frontend connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# root endpoint
@app.get("/")
def home():
    return {"message": "Phishing Detection API is running"}


# prediction endpoint
@app.post("/predict")
def predict(data: URLInput):
    try:
        logger.info(f"Received URL: {data.url}")
        result = int(predict_url(data.url))
        logger.info(f"Prediction Results: {result}")

        return {"url": data.url, "prediction": result}

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {"error": str(e)}
