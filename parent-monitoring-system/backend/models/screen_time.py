from datetime import datetime

from pydantic import BaseModel, Field


class ScreenTimeBase(BaseModel):
    child_id: str
    daily_limit: int = Field(..., ge=0, le=1440, description="Daily limit in minutes")


class ScreenTimeCreate(ScreenTimeBase):
    pass


class ScreenTime(ScreenTimeBase):
    id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True
