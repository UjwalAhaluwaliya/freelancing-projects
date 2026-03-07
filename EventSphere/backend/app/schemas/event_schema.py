from pydantic import BaseModel
from datetime import date

class EventCreate(BaseModel):
    title: str
    description: str
    category: str
    max_participants: int
    registration_deadline: date