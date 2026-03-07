from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ShipmentCreate(BaseModel):
    origin: str
    destination: str
    origin_lat: Optional[float] = None
    origin_lng: Optional[float] = None
    dest_lat: Optional[float] = None
    dest_lng: Optional[float] = None
    weight: float
    priority: str = "normal"
    customer_id: Optional[int] = None


class ShipmentOut(BaseModel):
    id: int
    tracking_number: str
    origin: str
    destination: str
    origin_lat: Optional[float] = None
    origin_lng: Optional[float] = None
    dest_lat: Optional[float] = None
    dest_lng: Optional[float] = None
    weight: float
    status: str
    priority: str
    customer_id: Optional[int] = None
    driver_id: Optional[int] = None
    vehicle_id: Optional[int] = None
    created_at: Optional[datetime] = None
    estimated_delivery: Optional[datetime] = None
    actual_delivery: Optional[datetime] = None

    class Config:
        from_attributes = True


class ShipmentUpdate(BaseModel):
    origin: Optional[str] = None
    destination: Optional[str] = None
    origin_lat: Optional[float] = None
    origin_lng: Optional[float] = None
    dest_lat: Optional[float] = None
    dest_lng: Optional[float] = None
    weight: Optional[float] = None
    status: Optional[str] = None
    priority: Optional[str] = None


class ShipmentAssign(BaseModel):
    driver_id: int
    vehicle_id: int
