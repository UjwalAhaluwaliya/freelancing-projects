from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class VehicleCreate(BaseModel):
    plate_number: str
    vehicle_type: str
    capacity: float
    fuel_type: str = "diesel"
    assigned_driver_id: Optional[int] = None


class VehicleOut(BaseModel):
    id: int
    plate_number: str
    vehicle_type: str
    capacity: float
    fuel_type: str
    fuel_level: float
    mileage: float
    status: str
    current_lat: Optional[float] = None
    current_lng: Optional[float] = None
    assigned_driver_id: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class VehicleUpdate(BaseModel):
    plate_number: Optional[str] = None
    vehicle_type: Optional[str] = None
    capacity: Optional[float] = None
    fuel_type: Optional[str] = None
    fuel_level: Optional[float] = None
    mileage: Optional[float] = None
    status: Optional[str] = None
    current_lat: Optional[float] = None
    current_lng: Optional[float] = None
    assigned_driver_id: Optional[int] = None
