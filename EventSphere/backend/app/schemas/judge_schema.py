from pydantic import BaseModel

class AssignJudge(BaseModel):
    event_id: str
    judge_id: str