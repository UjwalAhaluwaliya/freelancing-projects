from __future__ import annotations

from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


def _bootstrap_success_labels(df: pd.DataFrame) -> np.ndarray:
    base = 0.5 * df["ahp_score"] + 0.3 * df["expected_roi_norm"] + 0.2 * df["risk_benefit_norm"]
    return (base >= 0.55).astype(int).values


def predict_success_probability(df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
    if df.empty:
        return np.array([]), np.array([])

    features = df[
        [
            "budget_norm",
            "expected_roi_norm",
            "team_size_norm",
            "duration_norm",
            "strategic_alignment_score_norm",
            "risk_benefit_norm",
            "ahp_score",
        ]
    ].values
    labels = _bootstrap_success_labels(df)

    clf = RandomForestClassifier(n_estimators=200, random_state=42)
    clf.fit(features, labels)
    probs = clf.predict_proba(features)

    success_prob = probs[:, 1]
    feature_importance = clf.feature_importances_
    return success_prob, feature_importance
