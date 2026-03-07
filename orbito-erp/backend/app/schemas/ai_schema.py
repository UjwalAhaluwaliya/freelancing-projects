from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class JobDescriptionRequest(BaseModel):
    title: str
    skills: str
    experience: str
    department: str


class ResumeScoreRequest(BaseModel):
    resume_text: str = Field(min_length=1)
    job_description: str = Field(min_length=1)
    candidate_id: Optional[UUID] = None
    application_id: Optional[UUID] = None
    shortlist_threshold: int = Field(default=70, ge=0, le=100)


class PolicyChatRequest(BaseModel):
    question: str = Field(min_length=2)
