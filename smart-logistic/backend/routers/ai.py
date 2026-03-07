from fastapi import APIRouter, Depends, Query
from models.user import User
from schemas.ai import (
    RouteOptimizeRequest, RouteOptimizeResponse,
    ETAPredictRequest, ETAPredictResponse,
    DemandForecastResponse,
)
from services.auth import get_current_user
from ai.route_optimizer import optimize_route
from ai.demand_forecast import forecast_demand
from ai.eta_predictor import predict_eta

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/optimize-route", response_model=RouteOptimizeResponse)
def route_optimization(
    data: RouteOptimizeRequest,
    current_user: User = Depends(get_current_user),
):
    depot = (data.depot.lat, data.depot.lng)
    stops = [(s.lat, s.lng) for s in data.stops]
    stop_names = [s.name for s in data.stops]
    
    result = optimize_route(depot, stops, stop_names, data.num_vehicles)
    
    return RouteOptimizeResponse(
        optimized_order=[
            {"name": loc["name"], "lat": loc["lat"], "lng": loc["lng"]}
            for loc in result["optimized_order"]
        ],
        total_distance_km=result["total_distance_km"],
        route_polyline=result["route_polyline"],
    )


@router.get("/demand-forecast", response_model=DemandForecastResponse)
def get_demand_forecast(
    days: int = Query(default=30, ge=1, le=90),
    current_user: User = Depends(get_current_user),
):
    result = forecast_demand(days)
    return DemandForecastResponse(**result)


@router.post("/predict-eta", response_model=ETAPredictResponse)
def get_eta_prediction(
    data: ETAPredictRequest,
    current_user: User = Depends(get_current_user),
):
    result = predict_eta(
        distance_km=data.distance_km,
        traffic_factor=data.traffic_factor,
        weather_factor=data.weather_factor,
        vehicle_type=data.vehicle_type,
        load_weight_kg=data.load_weight_kg,
    )
    return ETAPredictResponse(**result)
