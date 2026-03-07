from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class InterviewCreate(BaseModel):
    application_id: UUID
    interviewer_name: str
    interview_date: datetime

class InterviewUpdate(BaseModel):
    status: Optional[str] = None
    feedback: Optional[str] = None
    score: Optional[float] = None