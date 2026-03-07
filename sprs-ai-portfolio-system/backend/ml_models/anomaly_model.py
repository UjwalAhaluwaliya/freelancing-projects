from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest


def detect_anomalies(df: pd.DataFrame, contamination: float = 0.15) -> np.ndarray:
    if df.empty:
        return np.array([])

    if len(df) < 4:
        return np.ones(len(df), dtype=int)

    features = df[
        [
            "budget_norm",
            "expected_roi_norm",
            "duration_norm",
            "risk_benefit_norm",
            "team_size_norm",
        ]
    ]
    model = IsolationForest(contamination=contamination, random_state=42)
    return model.fit_predict(features)
