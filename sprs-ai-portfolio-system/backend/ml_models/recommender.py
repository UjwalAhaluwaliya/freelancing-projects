from __future__ import annotations

from typing import Dict, List, Set

import numpy as np
import pandas as pd


def _label_from_scores(ahp_score: float, success_prob: float) -> str:
    blended = 0.55 * ahp_score + 0.45 * success_prob
    if blended >= 0.78:
        return "RETAIN"
    if blended >= 0.62:
        return "ENHANCE"
    if blended >= 0.46:
        return "CONSOLIDATE"
    if blended >= 0.3:
        return "DEFER"
    return "RETIRE"


def build_recommendations(
    df: pd.DataFrame,
    ahp_scores: pd.Series,
    success_probs: np.ndarray,
    clusters: np.ndarray,
    anomalies: np.ndarray,
    sim_matrix: np.ndarray,
    similar_pairs: List[Dict],
    optimization_selected: Set[str],
) -> List[Dict]:
    if df.empty:
        return []

    ranks = df["ahp_score"].rank(ascending=False, method="dense").astype(int)

    recommendations: List[Dict] = []
    for idx in range(len(df)):
        pid = str(df.iloc[idx]["_id"])
        project_name = str(df.iloc[idx].get("project_name", "Unnamed Project"))
        base_decision = _label_from_scores(float(ahp_scores.iloc[idx]), float(success_probs[idx]))
        final_decision = base_decision

        is_anomaly = bool(anomalies[idx] == -1)
        is_selected = pid in optimization_selected
        top_similarity = 0.0
        similar_project_id = None
        similar_project_name = None

        if len(df) > 1:
            sim_scores = sim_matrix[idx].copy()
            sim_scores[idx] = -1.0
            top_pos = int(np.argmax(sim_scores))
            top_similarity = float(sim_scores[top_pos])
            similar_project_id = str(df.iloc[top_pos]["_id"])
            similar_project_name = str(df.iloc[top_pos].get("project_name", "Unnamed Project"))

        # Decision fusion rules
        if is_anomaly and final_decision in {"RETAIN", "ENHANCE"}:
            final_decision = "DEFER"
        if top_similarity >= 0.8 and float(ahp_scores.iloc[idx]) < 0.65:
            final_decision = "CONSOLIDATE"
        if not is_selected and final_decision in {"RETAIN", "ENHANCE"}:
            final_decision = "DEFER"
        if float(ahp_scores.iloc[idx]) < 0.22:
            final_decision = "RETIRE"

        recommendations.append(
            {
                "project_id": pid,
                "project_name": project_name,
                "decision": final_decision,
                "confidence_score": round(float(success_probs[idx]), 4),
                "priority_rank": int(ranks.iloc[idx]),
                "rationale": {
                    "ahp_score": round(float(ahp_scores.iloc[idx]), 4),
                    "success_probability": round(float(success_probs[idx]), 4),
                    "cluster_id": int(clusters[idx]) if len(clusters) else 0,
                    "anomaly_flag": is_anomaly,
                    "similar_project_id": similar_project_id,
                    "similar_project_name": similar_project_name,
                    "similarity_score": round(top_similarity, 4),
                    "optimized_selection": is_selected,
                    "top_factors": ["roi", "strategic_alignment", "risk", "cost"],
                },
            }
        )

    return recommendations
