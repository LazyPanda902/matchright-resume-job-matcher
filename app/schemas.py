"""
MatchRight Schemas
Author: Ali Bidhendi

Notes:
- These define the request/response shapes for the API.
- FastAPI uses these to validate data and auto-generate docs.
"""

from pydantic import BaseModel
from typing import List


class MatchRequest(BaseModel):
    resume_text: str
    job_text: str


class MatchResponse(BaseModel):
    score: float
    missing_keywords: List[str]
    top_resume_keywords: List[str]
    top_job_keywords: List[str]
    suggestions: List[str]
