from pydantic import BaseModel, EmailStr
from typing import Optional

class ProfileCreate(BaseModel):
    email: EmailStr
    full_name: str
    role: str
    department: Optional[str] = None


class ProfileAdminUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[str] = None
    department: Optional[str] = None
    password: Optional[str] = None
