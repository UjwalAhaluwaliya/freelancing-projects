from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class ParentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr


class ParentCreate(ParentBase):
    password: str = Field(..., min_length=8, max_length=128)


class Parent(ParentBase):
    id: str
    phone: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True


class ParentInDB(Parent):
    hashed_password: str


class ParentProfileUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(default=None, max_length=20)
