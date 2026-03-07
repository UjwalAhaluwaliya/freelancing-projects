from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class ApplicationCreate(BaseModel):
    candidate_id: UUID
    job_id: UUID

class StageUpdate(BaseModel):
    stage: str