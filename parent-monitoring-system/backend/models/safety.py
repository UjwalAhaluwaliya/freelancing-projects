from pydantic import BaseModel, Field


class CheckUrlRequest(BaseModel):
    """Request body for POST /check-url (parent)."""

    url: str = Field(..., min_length=1, max_length=2048)
    child_id: str


class ChildCheckUrlRequest(BaseModel):
    """Request body for POST /child/check-url (child token, no child_id needed)."""

    url: str = Field(..., min_length=1, max_length=2048)


class DetectToxicRequest(BaseModel):
    """Request body for POST /detect-toxic."""

    text: str = Field(..., min_length=1, max_length=5000)
    child_id: str
