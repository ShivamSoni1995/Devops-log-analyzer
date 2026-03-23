# DevOps Log Analyzer AI Agent

## 🚀 Overview
This project is a simple AI agent built using Gemini that analyzes DevOps logs and provides:
- Issue
- Cause
- Fix
- Severity

## 🧠 Tech Stack
- FastAPI
- Google Gemini
- Docker
- Cloud Run

## 📦 Run Locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 🌐 API

POST /analyze

Request:
{
  "log": "OOMKilled container"
}

## ☁️ Deploy

Use Google Cloud Run for deployment.

