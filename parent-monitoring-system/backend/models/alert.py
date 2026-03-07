from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class AlertBase(BaseModel):
    child_id: str
    message: str = Field(..., min_length=1, max_length=500)
    alert_type: Optional[str] = Field(
        default=None,
        description="blocked_website | toxic_message | screen_time_exceeded",
    )


class AlertCreate(AlertBase):
    pass


class Alert(AlertBase):
    id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True
