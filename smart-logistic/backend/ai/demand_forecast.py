"""
Demand Forecasting using Scikit-learn
Models: Linear Regression and Random Forest
Predicts future shipment volumes based on historical patterns.
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ml_models")


def generate_synthetic_data(num_days: int = 365) -> pd.DataFrame:
    """Generate synthetic historical shipment data for training."""
    np.random.seed(42)
    dates = [datetime(2025, 1, 1) + timedelta(days=i) for i in range(num_days)]
    
    data = []
    for date in dates:
        day_of_week = date.weekday()
        month = date.month
        is_weekend = 1 if day_of_week >= 5 else 0
        is_holiday = 1 if (month == 12 and date.day in [24, 25, 31]) or (month == 1 and date.day == 1) else 0
        
        # Base demand with seasonal patterns
        base = 50
        seasonal = 15 * np.sin(2 * np.pi * month / 12)  # Seasonal trend
        weekly = -10 if is_weekend else 5 * np.sin(2 * np.pi * day_of_week / 5)
        holiday_effect = -20 if is_holiday else 0
        noise = np.random.normal(0, 5)
        
        shipment_count = max(5, int(base + seasonal + weekly + holiday_effect + noise))
        
        data.append({
            "date": date,
            "day_of_week": day_of_week,
            "month": month,
            "day_of_month": date.day,
            "is_weekend": is_weekend,
            "is_holiday": is_holiday,
            "shipment_count": shipment_count,
        })
    
    return pd.DataFrame(data)


def train_models():
    """Train Linear Regression and Random Forest models on synthetic data."""
    df = generate_synthetic_data()
    
    features = ["day_of_week", "month", "day_of_month", "is_weekend", "is_holiday"]
    X = df[features].values
    y = df["shipment_count"].values
    
    # Train Linear Regression
    lr_model = LinearRegression()
    lr_model.fit(X, y)
    
    # Train Random Forest
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
    rf_model.fit(X, y)
    
    # Save models
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(lr_model, os.path.join(MODEL_DIR, "demand_lr.pkl"))
    joblib.dump(rf_model, os.path.join(MODEL_DIR, "demand_rf.pkl"))
    
    return lr_model, rf_model


def load_models():
    """Load trained models from disk, or train new ones if not found."""
    lr_path = os.path.join(MODEL_DIR, "demand_lr.pkl")
    rf_path = os.path.join(MODEL_DIR, "demand_rf.pkl")
    
    if os.path.exists(lr_path) and os.path.exists(rf_path):
        return joblib.load(lr_path), joblib.load(rf_path)
    
    return train_models()


def forecast_demand(days_ahead: int = 30) -> dict:
    """
    Predict shipment demand for the next N days.
    
    Returns:
        dict with dates, predicted_shipments_lr, predicted_shipments_rf
    """
    lr_model, rf_model = load_models()
    
    start_date = datetime.utcnow() + timedelta(days=1)
    dates = []
    features_list = []
    
    for i in range(days_ahead):
        date = start_date + timedelta(days=i)
        day_of_week = date.weekday()
        month = date.month
        is_weekend = 1 if day_of_week >= 5 else 0
        is_holiday = 1 if (month == 12 and date.day in [24, 25, 31]) or (month == 1 and date.day == 1) else 0
        
        dates.append(date.strftime("%Y-%m-%d"))
        features_list.append([day_of_week, month, date.day, is_weekend, is_holiday])
    
    X = np.array(features_list)
    
    predictions_lr = lr_model.predict(X)
    predictions_rf = rf_model.predict(X)
    
    return {
        "dates": dates,
        "predicted_shipments_lr": [round(max(0, p), 1) for p in predictions_lr.tolist()],
        "predicted_shipments_rf": [round(max(0, p), 1) for p in predictions_rf.tolist()],
    }
