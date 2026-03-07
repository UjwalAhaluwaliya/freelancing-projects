from pydantic import BaseModel

class CriteriaCreate(BaseModel):
    title: str
    description: str | None = None