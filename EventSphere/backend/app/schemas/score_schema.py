from pydantic import BaseModel

class ScoreCreate(BaseModel):
    event_id: str
    participant_id: str
    criteria_id: str
    score: int