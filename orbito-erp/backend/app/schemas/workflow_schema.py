from typing import List, Optional
from pydantic import BaseModel, Field


class ResumeShortlistCandidate(BaseModel):
    id: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class ResumeShortlistApplication(BaseModel):
    id: Optional[str] = None
    stage: Optional[str] = None
    job_id: Optional[str] = None
    candidate_id: Optional[str] = None


class ResumeShortlistAnalysis(BaseModel):
    match_score: int = Field(ge=0, le=100)
    recommendation: str
    summary: str = ""
    strengths: List[str] = []
    missing_skills: List[str] = []
    raw_output: str = ""


class ResumeShortlistPayload(BaseModel):
    event_version: str
    triggered_at: str
    threshold: int = Field(ge=0, le=100)
    hr_user_id: str
    candidate: ResumeShortlistCandidate
    application: ResumeShortlistApplication
    analysis: ResumeShortlistAnalysis
