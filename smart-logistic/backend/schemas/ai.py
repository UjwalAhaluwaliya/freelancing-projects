from pydantic import BaseModel
from typing import List, Optional


class Location(BaseModel):
    name: str
    lat: float
    lng: float


class RouteOptimizeRequest(BaseModel):
    depot: Location
    stops: List[Location]
    num_vehicles: int = 1


class RouteOptimizeResponse(BaseModel):
    optimized_order: List[Location]
    total_distance_km: float
    route_polyline: List[List[float]]  # list of [lat, lng]


class ETAPredictRequest(BaseModel):
    distance_km: float
    traffic_factor: float = 1.0  # 1.0 = normal, >1 = heavy
    weather_factor: float = 1.0  # 1.0 = clear, >1 = bad weather
    vehicle_type: str = "truck"
    load_weight_kg: float = 100.0


class ETAPredictResponse(BaseModel):
    estimated_hours: float
    estimated_minutes: float


class DemandForecastResponse(BaseModel):
    dates: List[str]
    predicted_shipments_lr: List[float]  # Linear Regression
    predicted_shipments_rf: List[float]  # Random Forest
