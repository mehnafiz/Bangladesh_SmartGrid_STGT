"""Per-node feature extraction."""

from __future__ import annotations

import numpy as np
import pandas as pd

from constants import N_NODES, NODE_FEATURES_PER_REGION, REGIONS
from features.specs import node_feature_columns
from utils.exceptions import FeatureValidationError


class NodeFeatureBuilder:
    """Build (N, F_n) node feature matrices from a feature dataframe row slice."""

    def __init__(self) -> None:
        self.regions = REGIONS
        self.n_features = NODE_FEATURES_PER_REGION

    def build_frame(self, frame: pd.DataFrame) -> np.ndarray:
        """
        Build node features for all timesteps in frame.

        Returns array shaped (T, N, F_n).
        """
        if len(frame) == 0:
            raise FeatureValidationError("Cannot build node features from empty frame")

        tensor = np.empty((len(frame), N_NODES, self.n_features), dtype=np.float32)
        for t_idx in range(len(frame)):
            tensor[t_idx] = self.build_timestep(frame, t_idx)
        return tensor

    def build_timestep(self, frame: pd.DataFrame, t_idx: int) -> np.ndarray:
        """Build (N, F_n) node features for one timestep."""
        row = frame.iloc[t_idx]
        matrix = np.empty((N_NODES, self.n_features), dtype=np.float32)
        for n_idx, region in enumerate(self.regions):
            values = []
            for col in node_feature_columns(region):
                if col not in frame.columns:
                    raise FeatureValidationError(f"Missing node feature column: {col}")
                val = row[col]
                if pd.isna(val):
                    raise FeatureValidationError(
                        f"NaN in node feature {col} at index {t_idx}"
                    )
                values.append(float(val))
            matrix[n_idx] = np.asarray(values, dtype=np.float32)
        return matrix
