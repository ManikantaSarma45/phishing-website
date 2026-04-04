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

## Installation
Clone the repository
git clone https://github.com/YOUR_USERNAME/phishing-website.git
cd phishing-website

Create virtual environment
python3 -m venv venv
source venv/bin/activate

Install dependencies
pip install -r requirements.txt

## Running the Application
Start the FastAPI server
uvicorn backend.app.app:app --reload

Access API documentation
http://127.0.0.1:8000/docs

## Frontend
Open the frontend manually
open frontend/index.html

## API Usage
Endpoint
POST /predict

Request
{
  "url": "http://example.com"
}

Response
{
  "url": "http://example.com",
  "prediction": 0
}

## Docker
Build Docker image
docker build -t phishing-detector .

Run container
docker run -p 8000:8000 phishing-detector

Access API
http://localhost:8000/docs

## Machine Learning Pipeline
Run the complete pipeline
python backend/pipeline/pipeline.py

## Logging
Logs are stored in
backend/logs/app.log

## CI/CD
GitHub Actions workflow installs dependencies, validates code, and builds Docker image automatically.

## Model Details
- Models used: Random Forest and XGBoost
- Evaluation metrics: Accuracy, Precision, Recall, F1-score
- Final model stored as model_v1.pkl
