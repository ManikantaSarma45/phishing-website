# Phishing Website Detection System

## Overview
This project implements a machine learning-based system to detect phishing websites. Given a URL as input, the system classifies it as phishing, suspicious, or legitimate. The solution combines feature engineering, model training, and deployment using FastAPI and Docker.

## Features
- Multi-class classification of URLs
- Feature extraction using lexical, structural, statistical, and domain-based attributes
- Use of external data sources such as WHOIS, SSL, and Tranco ranking
- REST API built with FastAPI
- Docker-based deployment
- CI/CD pipeline using GitHub Actions

## Project Structure
```
phishing-website/
│
├── backend/
│   ├── app/
│   ├── src/
│   ├── models/
│   ├── pipeline/
│   └── logs/
│
├── frontend/
├── .github/workflows/
├── Dockerfile
├── requirements.txt
└── README.md
```

## Installation
Clone the repository
```bash
git clone https://github.com/ManikantaSarma45/phishing-website.git
cd phishing-website
```

Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies
```bash
pip install -r requirements.txt
```

## Running the Application
Start the FastAPI server
```bash
uvicorn backend.app.app:app --reload
```

Access API documentation
```bash
http://127.0.0.1:8000/docs
```

## Frontend
Open the frontend manually

open frontend/index.html

## API Usage
Endpoint
POST /predict

```
Request
{
  "url": "http://example.com"
}
```

Response
```
{
  "url": "http://example.com",
  "prediction": 0
}
```

## Docker
Build Docker image
```bash
docker build -t phishing-detector .
```

Run container
```bash
docker run -p 8000:8000 phishing-detector
```

Access API
```bash
http://localhost:8000/docs
```

## Machine Learning Pipeline
Run the complete pipeline
```bash
python -m backend.pipeline.pipeline
```
The model is trained and stored as `.pkl` files in `/backend/data` directory. The model evaluation and URL prediction results are logged in `/backend/logs/app.log` file.

## Logging
Logs are stored in
```bash
backend/logs/app.log
```

## CI/CD
GitHub Actions workflow installs dependencies, validates code, and builds Docker image automatically.

## Model Details
- Models used: Random Forest and XGBoost
- Evaluation metrics: Accuracy, Precision, Recall, F1-score
- Final model stored as model_v1.pkl
