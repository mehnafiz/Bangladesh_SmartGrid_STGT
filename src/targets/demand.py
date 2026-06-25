"""Regional demand target builder (raw MW from clean data)."""

from __future__ import annotations

import numpy as np
import pandas as pd

from constants import REGIONS
from targets.batch import YDemand
from utils.exceptions import TargetValidationError


class DemandTargetBuilder:
    """Extract h=1 demand targets from clean interim dataframe."""

    def __init__(self) -> None:
        self.regions = REGIONS

    def build(self, clean: pd.DataFrame, target_idx: int) -> YDemand:
        if target_idx < 0 or target_idx >= len(clean):
            raise TargetValidationError(f"target_idx out of range: {target_idx}")

        row = clean.iloc[target_idx]
        values = np.empty(len(self.regions), dtype=np.float32)
        for i, region in enumerate(self.regions):
            col = f"{region}_demand"
            if col not in clean.columns:
                raise TargetValidationError(f"Missing demand column: {col}")
            val = row[col]
            if pd.isna(val):
                raise TargetValidationError(f"NaN demand target for {region} at idx {target_idx}")
            if float(val) <= 0:
                raise TargetValidationError(
                    f"Non-positive demand for {region} at idx {target_idx}: {val}"
                )
            values[i] = float(val)
        return YDemand(values=values)
