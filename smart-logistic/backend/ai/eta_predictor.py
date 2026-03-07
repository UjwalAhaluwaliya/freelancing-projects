"""
ETA Prediction using Random Forest Regressor
Predicts estimated delivery time based on distance, traffic, weather, vehicle type, and load.
"""
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ml_models")

VEHICLE_TYPE_MAP = {"bike": 0, "van": 1, "truck": 2}


def generate_training_data(n_samples: int = 1000) -> tuple:
    """Generate synthetic training data for ETA prediction."""
    np.random.seed(42)
    
    distances = np.random.uniform(5, 500, n_samples)  # km
    traffic_factors = np.random.uniform(0.8, 2.5, n_samples)
    weather_factors = np.random.uniform(0.9, 2.0, n_samples)
    vehicle_types = np.random.choice([0, 1, 2], n_samples)  # 0=bike, 1=van, 2=truck
    load_weights = np.random.uniform(1, 5000, n_samples)  # kg
    
    # Base speed depends on vehicle type (km/h)
    base_speeds = np.where(vehicle_types == 0, 30, np.where(vehicle_types == 1, 60, 50))
    
    # Effective speed considering traffic and weather
    effective_speeds = base_speeds / (traffic_factors * weather_factors)
    
    # Load penalty: heavier loads slow down slightly
    load_penalty = 1 + (load_weights / 10000)
    
    # ETA in hours
    eta_hours = (distances / effective_speeds) * load_penalty
    # Add noise
    eta_hours += np.random.normal(0, 0.5, n_samples)
    eta_hours = np.maximum(eta_hours, 0.1)
    
    X = np.column_stack([distances, traffic_factors, weather_factors, vehicle_types, load_weights])
    y = eta_hours
    
    return X, y


def train_eta_model():
    """Train the ETA prediction model."""
    X, y = generate_training_data()
    
    model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=15)
    model.fit(X, y)
    
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, os.path.join(MODEL_DIR, "eta_rf.pkl"))
    
    return model


def load_eta_model():
    """Load trained ETA model from disk, or train if not found."""
    model_path = os.path.join(MODEL_DIR, "eta_rf.pkl")
    if os.path.exists(model_path):
        return joblib.load(model_path)
    return train_eta_model()


def predict_eta(distance_km: float, traffic_factor: float = 1.0, 
                weather_factor: float = 1.0, vehicle_type: str = "truck",
                load_weight_kg: float = 100.0) -> dict:
    """
    Predict estimated time of arrival.
    
    Args:
        distance_km: distance to destination in km
        traffic_factor: 1.0 = normal, >1 = heavy traffic
        weather_factor: 1.0 = clear, >1 = bad weather
        vehicle_type: bike, van, or truck
        load_weight_kg: weight of cargo in kg
    
    Returns:
        dict with estimated_hours and estimated_minutes
    """
    model = load_eta_model()
    
    vtype = VEHICLE_TYPE_MAP.get(vehicle_type.lower(), 2)
    X = np.array([[distance_km, traffic_factor, weather_factor, vtype, load_weight_kg]])
    
    prediction = model.predict(X)[0]
    hours = max(0.1, round(prediction, 2))
    
    return {
        "estimated_hours": hours,
        "estimated_minutes": round(hours * 60, 1),
    }
