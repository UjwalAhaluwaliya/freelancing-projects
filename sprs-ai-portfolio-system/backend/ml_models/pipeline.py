from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np

from ml_models.ahp_model import compute_ahp_scores
from ml_models.anomaly_model import detect_anomalies
from ml_models.clustering_model import cluster_projects
from ml_models.data_prep import prepare_project_frame
from ml_models.optimization_model import optimize_project_selection
from ml_models.random_forest_model import predict_success_probability
from ml_models.recommender import build_recommendations
from ml_models.similarity_model import compute_similarity


DECISIONS = ["RETAIN", "ENHANCE", "CONSOLIDATE", "DEFER", "RETIRE"]


def _decision_summary(recommendations: List[Dict]) -> Dict[str, int]:
    return {
        f"{decision.lower()}_count": int(sum(1 for rec in recommendations if rec["decision"] == decision))
        for decision in DECISIONS
    }


def run_analysis(projects: List[Dict]) -> Tuple[Dict, List[Dict]]:
    df = prepare_project_frame(projects)
    if df.empty:
        return {"summary": {}, "model_outputs": {}}, []

    ahp_scores, ahp_weights = compute_ahp_scores(df)
    df["ahp_score"] = ahp_scores

    success_probs, feature_importance = predict_success_probability(df)
    clusters = cluster_projects(df)
    anomalies = detect_anomalies(df)
    sim_matrix, similar_pairs = compute_similarity(df, threshold=0.75)

    budget_cap = float(df["budget"].sum() * 0.65)
    blocked = {str(df.iloc[idx]["_id"]) for idx in range(len(df)) if anomalies[idx] == -1}
    utility = (0.55 * np.array(ahp_scores) + 0.45 * success_probs).tolist()
    optimization = optimize_project_selection(
        project_ids=df["_id"].astype(str).tolist(),
        budgets=df["budget"].astype(float).tolist(),
        utilities=utility,
        max_budget=budget_cap,
        blocked_ids=blocked,
    )

    recommendations = build_recommendations(
        df=df,
        ahp_scores=ahp_scores,
        success_probs=success_probs,
        clusters=clusters,
        anomalies=anomalies,
        sim_matrix=sim_matrix,
        similar_pairs=similar_pairs,
        optimization_selected=set(optimization.get("selected_projects", [])),
    )

    model_outputs = {
        "ahp": {
            "weights": {k: round(v, 4) for k, v in ahp_weights.items()},
            "scores": [
                {
                    "project_id": str(df.iloc[idx]["_id"]),
                    "score": round(float(ahp_scores.iloc[idx]), 4),
                }
                for idx in range(len(df))
            ],
        },
        "random_forest": {
            "success_probability": [
                {
                    "project_id": str(df.iloc[idx]["_id"]),
                    "probability": round(float(success_probs[idx]), 4),
                }
                for idx in range(len(df))
            ],
            "feature_importance": {
                "budget_norm": round(float(feature_importance[0]), 4),
                "expected_roi_norm": round(float(feature_importance[1]), 4),
                "team_size_norm": round(float(feature_importance[2]), 4),
                "duration_norm": round(float(feature_importance[3]), 4),
                "strategic_alignment_score_norm": round(float(feature_importance[4]), 4),
                "risk_benefit_norm": round(float(feature_importance[5]), 4),
                "ahp_score": round(float(feature_importance[6]), 4),
            },
        },
        "kmeans": [
            {
                "project_id": str(df.iloc[idx]["_id"]),
                "cluster_id": int(clusters[idx]),
            }
            for idx in range(len(df))
        ],
        "similarity": {
            "pairs_above_threshold": similar_pairs,
        },
        "isolation_forest": [
            {
                "project_id": str(df.iloc[idx]["_id"]),
                "is_anomaly": bool(anomalies[idx] == -1),
            }
            for idx in range(len(df))
        ],
        "linear_programming": optimization,
    }

    analysis_payload = {
        "summary": _decision_summary(recommendations),
        "model_outputs": model_outputs,
    }

    return analysis_payload, recommendations
