from __future__ import annotations

from typing import Dict, Tuple

import numpy as np
import pandas as pd


DEFAULT_PAIRWISE_MATRIX = np.array(
    [
        [1.0, 2.0, 2.0, 3.0],
        [0.5, 1.0, 1.0, 2.0],
        [0.5, 1.0, 1.0, 2.0],
        [1 / 3, 0.5, 0.5, 1.0],
    ]
)
CRITERIA_ORDER = ["roi", "risk", "strategic_alignment", "cost"]


def _ahp_weights(pairwise_matrix: np.ndarray) -> np.ndarray:
    eig_vals, eig_vecs = np.linalg.eig(pairwise_matrix)
    max_index = int(np.argmax(eig_vals.real))
    principal = np.abs(eig_vecs[:, max_index].real)
    return principal / principal.sum()


def compute_ahp_scores(df: pd.DataFrame, pairwise_matrix: np.ndarray | None = None) -> Tuple[pd.Series, Dict[str, float]]:
    if df.empty:
        return pd.Series(dtype=float), {}

    matrix = pairwise_matrix if pairwise_matrix is not None else DEFAULT_PAIRWISE_MATRIX
    weights = _ahp_weights(matrix)
    weight_map = {CRITERIA_ORDER[idx]: float(weights[idx]) for idx in range(len(CRITERIA_ORDER))}

    score = (
        weight_map["roi"] * df["expected_roi_norm"]
        + weight_map["risk"] * df["risk_benefit_norm"]
        + weight_map["strategic_alignment"] * df["strategic_alignment_score_norm"]
        + weight_map["cost"] * df["cost_efficiency_norm"]
    )
    return score, weight_map
