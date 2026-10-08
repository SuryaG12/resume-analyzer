"""GradeMyResume API server.

Serves the single-page frontend and exposes the analysis endpoints.
Run:  uvicorn app:app --reload        (from the backend/ directory)
"""
from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from matching_engine import match_resume_to_job
from ats_scorer import score_ats
from ai_insights import generate_insights

app = FastAPI(title="GradeMyResume API", version="1.0.0")


class AnalyzeRequest(BaseModel):
    resume_text: str = Field(min_length=1, max_length=60000)
    job_text: str = Field(min_length=1, max_length=60000)


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok", "version": "1.0.0"}


@app.post("/api/analyze")
def analyze(req: AnalyzeRequest) -> JSONResponse:
    match = match_resume_to_job(req.resume_text, req.job_text)
    ats = score_ats(req.resume_text)
    insights = generate_insights(req.resume_text, req.job_text, match, ats)
    return JSONResponse(
        {
            "match": match.to_dict(),
            "ats": ats.to_dict(),
            "insights": insights,
        }
    )


# Serve the frontend (../frontend) at / when present.
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
if FRONTEND_DIR.is_dir():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
