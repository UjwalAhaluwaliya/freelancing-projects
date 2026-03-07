"""
Seed the database with sample data for demonstration.
Run: python seed_data.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from datetime import datetime, timedelta
import random
from database import engine, SessionLocal, Base
from models.user import User
from models.vehicle import Vehicle
from models.shipment import Shipment
from models.tracking import TrackingUpdate
from models.notification import Notification
from services.auth import hash_password

# Create tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Clear existing data
db.query(TrackingUpdate).delete()
db.query(Notification).delete()
db.query(Shipment).delete()
db.query(Vehicle).delete()
db.query(User).delete()
db.commit()

print("Seeding users...")
users = [
    User(username="admin", email="admin@logistics.com", hashed_password=hash_password("admin123"),
         full_name="System Admin", phone="+1234567890", role="admin"),
    User(username="manager1", email="manager@logistics.com", hashed_password=hash_password("manager123"),
         full_name="John Manager", phone="+1234567891", role="manager"),
    User(username="driver1", email="driver1@logistics.com", hashed_password=hash_password("driver123"),
         full_name="Mike Driver", phone="+1234567892", role="driver"),
    User(username="driver2", email="driver2@logistics.com", hashed_password=hash_password("driver123"),
         full_name="Sarah Driver", phone="+1234567893", role="driver"),
    User(username="driver3", email="driver3@logistics.com", hashed_password=hash_password("driver123"),
         full_name="Tom Driver", phone="+1234567894", role="driver"),
    User(username="customer1", email="customer1@example.com", hashed_password=hash_password("customer123"),
         full_name="Alice Customer", phone="+1234567895", role="customer"),
    User(username="customer2", email="customer2@example.com", hashed_password=hash_password("customer123"),
         full_name="Bob Customer", phone="+1234567896", role="customer"),
]
db.add_all(users)
db.commit()
for u in users:
    db.refresh(u)

print("Seeding vehicles...")
vehicles = [
    Vehicle(plate_number="TRK-001", vehicle_type="truck", capacity=5000, fuel_type="diesel",
            fuel_level=85.0, mileage=12500, status="available", current_lat=28.6139, current_lng=77.2090,
            assigned_driver_id=users[2].id),
    Vehicle(plate_number="TRK-002", vehicle_type="truck", capacity=8000, fuel_type="diesel",
            fuel_level=60.0, mileage=34000, status="in_transit", current_lat=19.0760, current_lng=72.8777,
            assigned_driver_id=users[3].id),
    Vehicle(plate_number="VAN-001", vehicle_type="van", capacity=2000, fuel_type="petrol",
            fuel_level=45.0, mileage=8900, status="available", current_lat=12.9716, current_lng=77.5946,
            assigned_driver_id=users[4].id),
    Vehicle(plate_number="VAN-002", vehicle_type="van", capacity=1500, fuel_type="petrol",
            fuel_level=92.0, mileage=5600, status="maintenance", current_lat=22.5726, current_lng=88.3639),
    Vehicle(plate_number="BKE-001", vehicle_type="bike", capacity=50, fuel_type="electric",
            fuel_level=70.0, mileage=2100, status="available", current_lat=13.0827, current_lng=80.2707),
]
db.add_all(vehicles)
db.commit()
for v in vehicles:
    db.refresh(v)

print("Seeding shipments...")
cities = [
    ("New Delhi", 28.6139, 77.2090),
    ("Mumbai", 19.0760, 72.8777),
    ("Bangalore", 12.9716, 77.5946),
    ("Kolkata", 22.5726, 88.3639),
    ("Chennai", 13.0827, 80.2707),
    ("Hyderabad", 17.3850, 78.4867),
    ("Pune", 18.5204, 73.8567),
    ("Jaipur", 26.9124, 75.7873),
]

statuses = ["pending", "assigned", "in_transit", "delivered", "delivered", "delivered", "cancelled"]
priorities = ["low", "normal", "normal", "high", "urgent"]

shipments = []
for i in range(25):
    origin = random.choice(cities)
    dest = random.choice([c for c in cities if c != origin])
    status = random.choice(statuses)
    created = datetime.utcnow() - timedelta(days=random.randint(1, 60))
    est_delivery = created + timedelta(hours=random.randint(12, 72))
    actual_delivery = est_delivery - timedelta(hours=random.randint(-12, 24)) if status == "delivered" else None

    driver_id = random.choice([users[2].id, users[3].id, users[4].id]) if status in ["assigned", "in_transit", "delivered"] else None
    vehicle_id = random.choice([vehicles[0].id, vehicles[1].id, vehicles[2].id]) if driver_id else None

    s = Shipment(
        tracking_number=f"SHP-{random.randint(100000, 999999):06d}",
        origin=origin[0],
        destination=dest[0],
        origin_lat=origin[1],
        origin_lng=origin[2],
        dest_lat=dest[1],
        dest_lng=dest[2],
        weight=round(random.uniform(10, 3000), 1),
        status=status,
        priority=random.choice(priorities),
        customer_id=random.choice([users[5].id, users[6].id]),
        driver_id=driver_id,
        vehicle_id=vehicle_id,
        created_at=created,
        estimated_delivery=est_delivery,
        actual_delivery=actual_delivery,
    )
    shipments.append(s)

db.add_all(shipments)
db.commit()
for s in shipments:
    db.refresh(s)

print("Seeding tracking updates...")
for s in shipments:
    if s.status in ["in_transit", "delivered"]:
        num_updates = random.randint(3, 8)
        for j in range(num_updates):
            frac = j / max(num_updates - 1, 1)
            lat = s.origin_lat + frac * (s.dest_lat - s.origin_lat) + random.uniform(-0.01, 0.01)
            lng = s.origin_lng + frac * (s.dest_lng - s.origin_lng) + random.uniform(-0.01, 0.01)
            update = TrackingUpdate(
                shipment_id=s.id,
                latitude=round(lat, 6),
                longitude=round(lng, 6),
                status="in_transit" if j < num_updates - 1 else s.status,
                notes=f"Checkpoint {j + 1}",
                timestamp=s.created_at + timedelta(hours=j * 4),
            )
            db.add(update)

print("Seeding notifications...")
notification_types = [
    ("dispatch", "New Shipment Assigned", "A new shipment has been assigned to you."),
    ("delivery", "Shipment Delivered", "Shipment has been successfully delivered."),
    ("delay", "Delivery Delay Alert", "A shipment is experiencing delays due to traffic."),
    ("system", "System Update", "System maintenance scheduled for this weekend."),
]
for user in users:
    for _ in range(random.randint(2, 5)):
        ntype = random.choice(notification_types)
        n = Notification(
            user_id=user.id,
            title=ntype[1],
            message=ntype[2],
            notification_type=ntype[0],
            is_read=random.choice([True, False]),
            created_at=datetime.utcnow() - timedelta(hours=random.randint(1, 168)),
        )
        db.add(n)

db.commit()
db.close()

print("\n✓ Database seeded successfully!")
print("  - 7 users (admin/manager/drivers/customers)")
print("  - 5 vehicles")
print("  - 25 shipments")
print("  - Tracking updates & notifications")
print("\nLogin credentials:")
print("  Admin:    admin / admin123")
print("  Manager:  manager1 / manager123")
print("  Driver:   driver1 / driver123")
print("  Customer: customer1 / customer123")
