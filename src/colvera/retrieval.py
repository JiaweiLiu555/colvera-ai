"""Transparent, non-diagnostic historical-case retrieval for the research MMP."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler


def retrieve_neighbors(
    train: pd.DataFrame,
    query: pd.DataFrame,
    feature_columns: list[str],
    patient_id: str,
    outcome_column: str,
    neighbors: int = 3,
) -> pd.DataFrame:
    """Return only historical development-set cases, never the queried holdout case."""
    scaler = StandardScaler().fit(train[feature_columns])
    train_x = scaler.transform(train[feature_columns])
    query_x = scaler.transform(query[feature_columns])
    model = NearestNeighbors(n_neighbors=min(neighbors, len(train)), metric="euclidean").fit(train_x)
    distances, indices = model.kneighbors(query_x)
    rows = []
    for query_index, (distance_row, index_row) in enumerate(zip(distances, indices)):
        qid = int(query.iloc[query_index][patient_id])
        for rank, (distance, train_index) in enumerate(zip(distance_row, index_row), start=1):
            candidate = train.iloc[int(train_index)]
            rows.append(
                {
                    "query_patient_id": qid,
                    "rank": rank,
                    "neighbor_patient_id": int(candidate[patient_id]),
                    "euclidean_distance": float(distance),
                    "historical_outcome_binary": int(candidate[outcome_column]),
                }
            )
    return pd.DataFrame(rows)
