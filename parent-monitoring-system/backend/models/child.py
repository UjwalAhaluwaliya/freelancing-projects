from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
class ChildLoginRequest(BaseModel):
    child_id: str
    password: str
    parent_email: Optional[str] = None

class ChildBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=0, le=18)


class ChildCreate(ChildBase):
    password: str = Field(..., min_length=6, max_length=128)


class Child(ChildBase):
    id: str
    parent_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True


class ChildInDB(Child):
    hashed_password: str


