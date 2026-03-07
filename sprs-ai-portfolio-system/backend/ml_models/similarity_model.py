from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def compute_similarity(df: pd.DataFrame, threshold: float = 0.75) -> Tuple[np.ndarray, List[Dict]]:
    if df.empty:
        return np.array([[]]), []

    corpus = df["description"].fillna("").astype(str).tolist()
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(corpus)
    sim_matrix = cosine_similarity(tfidf_matrix)

    pairs: List[Dict] = []
    for i in range(len(df)):
        for j in range(i + 1, len(df)):
            score = float(sim_matrix[i, j])
            if score >= threshold:
                pairs.append(
                    {
                        "project_a": str(df.iloc[i]["_id"]),
                        "project_b": str(df.iloc[j]["_id"]),
                        "cosine_similarity": round(score, 4),
                    }
                )

    return sim_matrix, pairs
