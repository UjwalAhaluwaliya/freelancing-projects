from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans


def cluster_projects(df: pd.DataFrame, max_clusters: int = 4) -> np.ndarray:
    if df.empty:
        return np.array([])

    n_samples = len(df)
    n_clusters = max(1, min(max_clusters, n_samples))
    if n_clusters == 1:
        return np.zeros(n_samples, dtype=int)

    features = df[
        [
            "budget_norm",
            "expected_roi_norm",
            "team_size_norm",
            "duration_norm",
            "strategic_alignment_score_norm",
            "risk_benefit_norm",
        ]
    ]

    model = KMeans(n_clusters=n_clusters, n_init=10, random_state=42)
    return model.fit_predict(features)
