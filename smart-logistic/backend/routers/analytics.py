from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from database import get_db
from models.shipment import Shipment
from models.vehicle import Vehicle
from models.user import User
from services.auth import get_current_user

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/summary")
def get_summary(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    total_shipments = db.query(Shipment).count()
    pending = db.query(Shipment).filter(Shipment.status == "pending").count()
    in_transit = db.query(Shipment).filter(Shipment.status == "in_transit").count()
    delivered = db.query(Shipment).filter(Shipment.status == "delivered").count()
    cancelled = db.query(Shipment).filter(Shipment.status == "cancelled").count()

    total_vehicles = db.query(Vehicle).count()
    active_vehicles = db.query(Vehicle).filter(Vehicle.status == "in_transit").count()
    available_vehicles = db.query(Vehicle).filter(Vehicle.status == "available").count()
    maintenance_vehicles = db.query(Vehicle).filter(Vehicle.status == "maintenance").count()

    total_drivers = db.query(User).filter(User.role == "driver").count()

    # On-time rate
    on_time = db.query(Shipment).filter(
        Shipment.status == "delivered",
        Shipment.actual_delivery <= Shipment.estimated_delivery
    ).count()
    on_time_rate = round((on_time / delivered * 100), 1) if delivered > 0 else 0

    return {
        "total_shipments": total_shipments,
        "pending": pending,
        "in_transit": in_transit,
        "delivered": delivered,
        "cancelled": cancelled,
        "total_vehicles": total_vehicles,
        "active_vehicles": active_vehicles,
        "available_vehicles": available_vehicles,
        "maintenance_vehicles": maintenance_vehicles,
        "total_drivers": total_drivers,
        "on_time_rate": on_time_rate,
    }


@router.get("/delivery-performance")
def delivery_performance(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Delivery status breakdown for pie chart."""
    statuses = ["pending", "assigned", "in_transit", "delivered", "cancelled"]
    result = []
    for status in statuses:
        count = db.query(Shipment).filter(Shipment.status == status).count()
        result.append({"status": status, "count": count})
    return result


@router.get("/fuel-report")
def fuel_report(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Fuel levels by vehicle for bar chart."""
    vehicles = db.query(Vehicle).all()
    return [
        {
            "plate_number": v.plate_number,
            "vehicle_type": v.vehicle_type,
            "fuel_level": v.fuel_level,
            "mileage": v.mileage,
        }
        for v in vehicles
    ]


@router.get("/trends")
def trends(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Monthly shipment trends for line chart."""
    # Get shipment counts grouped by month
    results = (
        db.query(
            extract("month", Shipment.created_at).label("month"),
            func.count(Shipment.id).label("count"),
        )
        .group_by(extract("month", Shipment.created_at))
        .order_by(extract("month", Shipment.created_at))
        .all()
    )

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    month_data = {i + 1: 0 for i in range(12)}
    for row in results:
        if row.month:
            month_data[int(row.month)] = row.count

    return [{"month": months[i], "shipments": month_data[i + 1]} for i in range(12)]
