from pydantic import BaseModel, EmailStr
from typing import Optional, List

class CandidateCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    skills: Optional[List[str]] = []
    total_experience: Optional[int] = None
    resume_url: Optional[str] = None

class CandidateUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    skills: Optional[List[str]] = None
    total_experience: Optional[int] = None
    resume_url: Optional[str] = None
    overall_score: Optional[float] = None
    recommendation: Optional[str] = None