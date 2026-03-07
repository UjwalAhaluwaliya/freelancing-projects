import uuid
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models.shipment import Shipment
from models.vehicle import Vehicle
from models.notification import Notification
from models.user import User
from schemas.shipment import ShipmentCreate, ShipmentOut, ShipmentUpdate, ShipmentAssign
from services.auth import get_current_user

router = APIRouter(prefix="/shipments", tags=["Shipments"])


def generate_tracking_number():
    return "SHP-" + uuid.uuid4().hex[:10].upper()


@router.get("/", response_model=List[ShipmentOut])
def list_shipments(
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Shipment)
    if current_user.role == "customer":
        query = query.filter(Shipment.customer_id == current_user.id)
    elif current_user.role == "driver":
        query = query.filter(Shipment.driver_id == current_user.id)
    if status:
        query = query.filter(Shipment.status == status)
    return query.order_by(Shipment.created_at.desc()).offset(skip).limit(limit).all()


@router.post("/", response_model=ShipmentOut)
def create_shipment(
    data: ShipmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    shipment = Shipment(
        tracking_number=generate_tracking_number(),
        origin=data.origin,
        destination=data.destination,
        origin_lat=data.origin_lat,
        origin_lng=data.origin_lng,
        dest_lat=data.dest_lat,
        dest_lng=data.dest_lng,
        weight=data.weight,
        priority=data.priority,
        customer_id=data.customer_id or current_user.id,
    )
    db.add(shipment)
    db.commit()
    db.refresh(shipment)
    return shipment


@router.get("/{shipment_id}", response_model=ShipmentOut)
def get_shipment(shipment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return shipment


@router.put("/{shipment_id}", response_model=ShipmentOut)
def update_shipment(
    shipment_id: int,
    data: ShipmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(shipment, key, value)

    # If status changed to delivered, set actual_delivery
    if data.status == "delivered":
        shipment.actual_delivery = datetime.utcnow()

    db.commit()
    db.refresh(shipment)
    return shipment


@router.post("/{shipment_id}/assign", response_model=ShipmentOut)
def assign_shipment(
    shipment_id: int,
    data: ShipmentAssign,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")

    # Verify driver exists and is a driver
    driver = db.query(User).filter(User.id == data.driver_id, User.role == "driver").first()
    if not driver:
        raise HTTPException(status_code=400, detail="Invalid driver")

    # Verify vehicle exists and is available
    vehicle = db.query(Vehicle).filter(Vehicle.id == data.vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=400, detail="Invalid vehicle")

    shipment.driver_id = data.driver_id
    shipment.vehicle_id = data.vehicle_id
    shipment.status = "assigned"
    shipment.estimated_delivery = datetime.utcnow() + timedelta(hours=24)

    # Update vehicle status
    vehicle.status = "in_transit"

    # Create dispatch notification
    notification = Notification(
        user_id=data.driver_id,
        title="New Shipment Assigned",
        message=f"Shipment {shipment.tracking_number} has been assigned to you. Destination: {shipment.destination}",
        notification_type="dispatch",
    )
    db.add(notification)

    db.commit()
    db.refresh(shipment)
    return shipment
