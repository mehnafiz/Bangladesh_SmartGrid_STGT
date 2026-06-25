"""OSI target builder using Phase 05B frozen formula."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from constants import COL_EVE_PEAK, COL_HIGHEST_GEN, LIMITATION_COLS, REGIONS
from targets.batch import YOSI
from utils.exceptions import TargetValidationError
from utils.logging import get_logger

logger = get_logger(__name__)


@dataclass(frozen=True)
class OSIComponentBounds:
    c1: tuple[float, float]
    c2: tuple[float, float]
    c3: tuple[float, float]


class OSITargetBuilder:
    """
    Compute OSI(t+1) ∈ [0, 1] from clean raw columns.

    Component min-max bounds are fit on train split only (Phase 05B).
    """

    def __init__(self, train_clean: pd.DataFrame) -> None:
        self.bounds = self._fit_bounds(train_clean)
        logger.info(
            "Fitted OSI bounds on %s train rows", len(train_clean)
        )

    @staticmethod
    def _minmax(value: float, lo: float, hi: float) -> float:
        span = hi - lo
        if span <= 0:
            return 0.0
        return float(np.clip((value - lo) / span, 0.0, 1.0))

    def _fit_bounds(self, train_clean: pd.DataFrame) -> OSIComponentBounds:
        c1, c2, c3 = self._components(train_clean)
        return OSIComponentBounds(
            c1=(float(c1.min()), float(c1.max())),
            c2=(float(c2.min()), float(c2.max())),
            c3=(float(c3.min()), float(c3.max())),
        )

    @staticmethod
    def _components(df: pd.DataFrame) -> tuple[pd.Series, pd.Series, pd.Series]:
        demand_cols = [f"{r}_demand" for r in REGIONS]
        load_cols = [f"{r}_load" for r in REGIONS]
        total_demand = df[demand_cols].sum(axis=1)
        total_load = df[load_cols].sum(axis=1)
        generation_reserve = df[COL_HIGHEST_GEN] - df[COL_EVE_PEAK]
        total_limitation = df[list(LIMITATION_COLS)].sum(axis=1)

        c1 = total_load / total_demand.replace(0, np.nan)
        c2 = 1.0 - generation_reserve / df[COL_HIGHEST_GEN].replace(0, np.nan)
        c3 = total_limitation / df[COL_HIGHEST_GEN].replace(0, np.nan)
        return c1, c2, c3

    def build(self, clean: pd.DataFrame, target_idx: int) -> YOSI:
        if target_idx < 0 or target_idx >= len(clean):
            raise TargetValidationError(f"target_idx out of range: {target_idx}")

        row_df = clean.iloc[[target_idx]]
        c1, c2, c3 = self._components(row_df)
        if c1.isna().any() or c2.isna().any() or c3.isna().any():
            raise TargetValidationError(f"NaN OSI component at target_idx={target_idx}")

        n1 = self._minmax(float(c1.iloc[0]), *self.bounds.c1)
        n2 = self._minmax(float(c2.iloc[0]), *self.bounds.c2)
        n3 = self._minmax(float(c3.iloc[0]), *self.bounds.c3)
        osi = (n1 + n2 + n3) / 3.0
        return YOSI(value=float(osi))
