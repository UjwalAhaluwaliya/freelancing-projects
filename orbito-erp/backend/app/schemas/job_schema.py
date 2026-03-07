from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class JobCreate(BaseModel):
    title: str
    department_id: Optional[UUID] = None
    experience_level: Optional[str] = None
    location: Optional[str] = None
    employment_type: Optional[str] = None
    description: str

class JobUpdate(BaseModel):
    title: Optional[str] = None
    department_id: Optional[UUID] = None
    experience_level: Optional[str] = None
    location: Optional[str] = None
    employment_type: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None