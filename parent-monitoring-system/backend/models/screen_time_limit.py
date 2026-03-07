from datetime import date

from pydantic import BaseModel, Field


class SetLimitRequest(BaseModel):
    """Request body for POST /set-limit."""

    child_id: str
    daily_limit: int = Field(..., ge=0, le=1440, description="Daily limit in minutes")



class LogUsageRequest(BaseModel):

    usage_time: int

    date: str


class ResetUsageRequest(BaseModel):
    """Request body for POST /reset-usage."""

    child_id: str
    date: str | None = None
