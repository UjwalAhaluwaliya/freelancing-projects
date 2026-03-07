import random
import math
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.tracking import TrackingUpdate
from models.shipment import Shipment
from models.vehicle import Vehicle
from models.notification import Notification
from models.user import User
from schemas.tracking import TrackingUpdateCreate, TrackingUpdateOut
from services.auth import get_current_user

router = APIRouter(prefix="/tracking", tags=["Tracking"])


@router.get("/{shipment_id}", response_model=List[TrackingUpdateOut])
def get_tracking_history(
    shipment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    updates = db.query(TrackingUpdate).filter(
        TrackingUpdate.shipment_id == shipment_id
    ).order_by(TrackingUpdate.timestamp.asc()).all()
    return updates


@router.post("/{shipment_id}/update", response_model=TrackingUpdateOut)
def add_tracking_update(
    shipment_id: int,
    data: TrackingUpdateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")

    update = TrackingUpdate(
        shipment_id=shipment_id,
        latitude=data.latitude,
        longitude=data.longitude,
        status=data.status,
        notes=data.notes,
    )
    db.add(update)

    # Update vehicle position if assigned
    if shipment.vehicle_id:
        vehicle = db.query(Vehicle).filter(Vehicle.id == shipment.vehicle_id).first()
        if vehicle:
            vehicle.current_lat = data.latitude
            vehicle.current_lng = data.longitude

    db.commit()
    db.refresh(update)
    return update


@router.post("/simulate/{shipment_id}")
def simulate_tracking(
    shipment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Simulate GPS tracking by generating intermediate points between origin and destination."""
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")

    if not all([shipment.origin_lat, shipment.origin_lng, shipment.dest_lat, shipment.dest_lng]):
        raise HTTPException(status_code=400, detail="Shipment must have origin and destination coordinates")

    # Generate 10 intermediate points
    num_points = 10
    updates = []
    for i in range(num_points + 1):
        fraction = i / num_points
        lat = shipment.origin_lat + fraction * (shipment.dest_lat - shipment.origin_lat)
        lng = shipment.origin_lng + fraction * (shipment.dest_lng - shipment.origin_lng)
        # Add small random offset to simulate real movement
        lat += random.uniform(-0.005, 0.005)
        lng += random.uniform(-0.005, 0.005)

        status_text = "in_transit"
        if i == 0:
            status_text = "picked_up"
        elif i == num_points:
            status_text = "delivered"
            lat = shipment.dest_lat
            lng = shipment.dest_lng

        update = TrackingUpdate(
            shipment_id=shipment_id,
            latitude=round(lat, 6),
            longitude=round(lng, 6),
            status=status_text,
            notes=f"Simulated checkpoint {i + 1}/{num_points + 1}",
        )
        db.add(update)
        updates.append({"lat": round(lat, 6), "lng": round(lng, 6), "status": status_text})

    # Update shipment status
    shipment.status = "in_transit"

    # Update vehicle position to last point
    if shipment.vehicle_id:
        vehicle = db.query(Vehicle).filter(Vehicle.id == shipment.vehicle_id).first()
        if vehicle:
            vehicle.current_lat = updates[-1]["lat"]
            vehicle.current_lng = updates[-1]["lng"]

    db.commit()
    return {"message": "Simulation complete", "points": updates}
