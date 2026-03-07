from __future__ import annotations

from typing import Dict, List

import pandas as pd
from sklearn.preprocessing import MinMaxScaler


RISK_TO_NUMERIC = {"low": 1.0, "medium": 0.6, "high": 0.2}


def prepare_project_frame(projects: List[Dict]) -> pd.DataFrame:
    df = pd.DataFrame(projects).copy()
    if df.empty:
        return df

    if "_id" not in df.columns:
        df["_id"] = [str(i) for i in range(len(df))]
    df["_id"] = df["_id"].astype(str)

    numeric_cols = [
        "budget",
        "expected_roi",
        "team_size",
        "duration",
        "strategic_alignment_score",
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df.get(col), errors="coerce").fillna(0.0)

    df["description"] = df.get("description", "").fillna("").astype(str)
    df["risk_level"] = df.get("risk_level", "medium").fillna("medium").astype(str).str.lower()
    df["risk_numeric"] = df["risk_level"].map(RISK_TO_NUMERIC).fillna(0.5)

    scaler = MinMaxScaler()
    scale_cols = numeric_cols + ["risk_numeric"]
    scaled = scaler.fit_transform(df[scale_cols])
    scaled_df = pd.DataFrame(scaled, columns=[f"{c}_norm" for c in scale_cols], index=df.index)
    df = pd.concat([df, scaled_df], axis=1)

    # Cost is inverse of normalized budget to align with value orientation.
    df["cost_efficiency_norm"] = 1.0 - df["budget_norm"]
    df["risk_benefit_norm"] = df["risk_numeric_norm"]

    return df
