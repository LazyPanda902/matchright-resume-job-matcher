"""
MatchRight API
Author: Ali Bidhendi

Endpoints:
- GET /     : health check
- POST /match : compute match score + keyword gap + suggestions

Run:
uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from app.schemas import MatchRequest, MatchResponse
from app.nlp import similarity_score, keyword_gap_analysis, suggestions_from_missing

app = FastAPI(
    title="MatchRight API",
    version="1.0",
    description="Resume x Job matching API by Ali Bidhendi"
)


@app.get("/")
def home():
    return {
        "message": "MatchRight is running.",
        "author": "Ali Bidhendi",
        "endpoints": ["/match"]
    }


@app.post("/match", response_model=MatchResponse)
def match(req: MatchRequest) -> MatchResponse:
    score = similarity_score(req.resume_text, req.job_text)

    missing, resume_top, job_top = keyword_gap_analysis(
        req.resume_text,
        req.job_text,
        job_top_k=20
    )

    suggestions = suggestions_from_missing(missing)

    return MatchResponse(
        score=score,
        missing_keywords=missing,
        top_resume_keywords=resume_top,
        top_job_keywords=job_top,
        suggestions=suggestions
    )
