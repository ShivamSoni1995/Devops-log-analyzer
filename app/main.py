from fastapi import FastAPI
from app.schemas import LogRequest
from app.agent import analyze_log_agent

app = FastAPI()

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/analyze")
def analyze(request: LogRequest):
    return analyze_log_agent(request.log)
