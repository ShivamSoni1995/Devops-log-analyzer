from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.agent import analyze_log_agent
from app.schemas import LogAnalysis, LogRequest

app = FastAPI(title="DevOps Log Analyzer Agent")
static_dir = Path(__file__).resolve().parent / "static"

app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
def home() -> FileResponse:
    return FileResponse(static_dir / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/analyze", response_model=LogAnalysis)
async def analyze(request: LogRequest) -> LogAnalysis:
    return await analyze_log_agent(request.log)
