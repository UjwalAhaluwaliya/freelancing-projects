"""
Script to train all ML models and save them to disk.
Run this once before starting the server: python ai/train_models.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from ai.demand_forecast import train_models as train_demand_models
from ai.eta_predictor import train_eta_model

if __name__ == "__main__":
    print("Training demand forecasting models (Linear Regression + Random Forest)...")
    train_demand_models()
    print("✓ Demand models saved.")

    print("Training ETA prediction model (Random Forest)...")
    train_eta_model()
    print("✓ ETA model saved.")

    print("\nAll models trained and saved to ml_models/ directory.")
