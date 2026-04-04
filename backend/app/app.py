from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.schema import URLInput
from backend.src.predict import Predict

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
    result = int(Predict().predict(data.url))

    return {
        "url": data.url,
        "prediction": result
    }