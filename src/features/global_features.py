"""Global context feature extraction."""

from __future__ import annotations

import numpy as np
import pandas as pd

from constants import GLOBAL_FEATURES, HOLIDAY_CAT_COLUMNS
from features.leakage_guard import LeakageGuard
from features.specs import GLOBAL_INPUT_FEATURE_NAMES
from utils.exceptions import FeatureValidationError


class GlobalFeatureBuilder:
    """Build (F_g,) global vectors — 17 features including derived Holiday_cat."""

    def __init__(self) -> None:
        self.feature_names = GLOBAL_INPUT_FEATURE_NAMES
        self.n_features = GLOBAL_FEATURES
        LeakageGuard.validate_global_names()

    def build_frame(self, frame: pd.DataFrame) -> np.ndarray:
        """Build global features for all timesteps. Shape (T, F_g)."""
        tensor = np.empty((len(frame), self.n_features), dtype=np.float32)
        for t_idx in range(len(frame)):
            tensor[t_idx] = self.build_timestep(frame, t_idx)
        return tensor

    def build_timestep(self, frame: pd.DataFrame, t_idx: int) -> np.ndarray:
        row = frame.iloc[t_idx]
        values: list[float] = []
        for name in self.feature_names:
            if name == "Holiday_cat":
                values.append(self._decode_holiday_category(row))
            else:
                if name not in frame.columns:
                    raise FeatureValidationError(f"Missing global feature column: {name}")
                val = row[name]
                if pd.isna(val):
                    raise FeatureValidationError(
                        f"NaN in global feature {name} at index {t_idx}"
                    )
                values.append(float(val))
        return np.asarray(values, dtype=np.float32)

    @staticmethod
    def _decode_holiday_category(row: pd.Series) -> float:
        """Decode one-hot holiday columns to categorical index 0–3."""
        one_hot = row[list(HOLIDAY_CAT_COLUMNS)].astype(float).to_numpy()
        if one_hot.sum() == 0:
            return 0.0
        return float(np.argmax(one_hot))
