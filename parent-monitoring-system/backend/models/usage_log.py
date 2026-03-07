from datetime import date, datetime

from pydantic import BaseModel, Field


class UsageLogBase(BaseModel):
    child_id: str
    date: date
    usage_time: int = Field(..., ge=0, description="Usage time in minutes")


class UsageLogCreate(UsageLogBase):
    pass


class UsageLog(UsageLogBase):
    id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True
