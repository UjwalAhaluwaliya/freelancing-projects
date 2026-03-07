from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from database import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    plate_number = Column(String(20), unique=True, nullable=False)
    vehicle_type = Column(String(30), nullable=False)  # truck, van, bike
    capacity = Column(Float, nullable=False)  # in kg
    fuel_type = Column(String(20), nullable=False, default="diesel")  # diesel, petrol, electric
    fuel_level = Column(Float, default=100.0)  # percentage
    mileage = Column(Float, default=0.0)
    status = Column(String(20), default="available")  # available, in_transit, maintenance
    current_lat = Column(Float, nullable=True)
    current_lng = Column(Float, nullable=True)
    assigned_driver_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
