from pydantic import BaseModel, EmailStr, Field


class ParentLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1)


class ParentForgotPassword(BaseModel):
    email: EmailStr
    new_password: str = Field(..., min_length=8, max_length=128)


class ChildLogin(BaseModel):
    child_id: str
    password: str = Field(..., min_length=1)
