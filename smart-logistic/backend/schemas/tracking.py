from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TrackingUpdateCreate(BaseModel):
    latitude: float
    longitude: float
    status: Optional[str] = None
    notes: Optional[str] = None


class TrackingUpdateOut(BaseModel):
    id: int
    shipment_id: int
    latitude: float
    longitude: float
    timestamp: Optional[datetime] = None
    status: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True
