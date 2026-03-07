from pydantic import BaseModel

class EventCriteriaCreate(BaseModel):
    event_id: str
    criteria_id: str
    weight: float