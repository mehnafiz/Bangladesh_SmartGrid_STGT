"""Chronological split management and sample index generation."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from constants import FORECAST_HORIZON_H, INPUT_WINDOW_T, SPLIT_SPECS, WARMUP_SKIP
from utils.logging import get_logger

logger = get_logger(__name__)


@dataclass(frozen=True)
class SampleIndex:
    """A valid window end index and corresponding target index."""

    end_idx: int
    target_idx: int
    date_end: pd.Timestamp
    date_target: pd.Timestamp


class SplitManager:
    """Manage split boundaries and valid sample indices."""

    def __init__(self, window_size: int = INPUT_WINDOW_T, horizon: int = FORECAST_HORIZON_H) -> None:
        self.window_size = window_size
        self.horizon = horizon
        self.warmup = WARMUP_SKIP

    def validate_boundaries(self, splits: dict[str, pd.DataFrame]) -> None:
        """Ensure splits are chronological and non-overlapping."""
        ordered = sorted(SPLIT_SPECS.keys(), key=lambda k: SPLIT_SPECS[k].start_date)
        prev_end: pd.Timestamp | None = None
        for name in ordered:
            spec = SPLIT_SPECS[name]
            df = splits[name]
            start = pd.Timestamp(spec.start_date)
            end = pd.Timestamp(spec.end_date)
            actual_start = df["Date"].min()
            actual_end = df["Date"].max()
            if actual_start > start + pd.Timedelta(days=1):
                logger.warning(
                    "Split %s starts later than spec: %s vs %s",
                    name,
                    actual_start.date(),
                    start.date(),
                )
            if actual_end < end - pd.Timedelta(days=1):
                logger.warning(
                    "Split %s ends earlier than spec: %s vs %s",
                    name,
                    actual_end.date(),
                    end.date(),
                )
            if prev_end is not None and actual_start <= prev_end:
                raise ValueError(
                    f"Split overlap detected: {name} starts {actual_start} "
                    f"before previous end {prev_end}"
                )
            prev_end = actual_end

    def sample_indices(self, features: pd.DataFrame) -> list[SampleIndex]:
        """
        Return valid sample indices for a split.

        Window covers [end_idx - T + 1, end_idx]; target at end_idx + horizon.
        """
        dates = pd.to_datetime(features["Date"])
        min_end = self.warmup + self.window_size - 1
        max_end = len(features) - self.horizon - 1
        if max_end < min_end:
            return []

        indices: list[SampleIndex] = []
        for end_idx in range(min_end, max_end + 1):
            target_idx = end_idx + self.horizon
            indices.append(
                SampleIndex(
                    end_idx=end_idx,
                    target_idx=target_idx,
                    date_end=dates.iloc[end_idx],
                    date_target=dates.iloc[target_idx],
                )
            )
        logger.debug(
            "Generated %s sample indices (rows=%s, window=%s)",
            len(indices),
            len(features),
            self.window_size,
        )
        return indices

    def window_slice(self, end_idx: int) -> slice:
        """Return slice for temporal window ending at end_idx."""
        start = end_idx - self.window_size + 1
        if start < 0:
            raise ValueError(f"Window underflow at end_idx={end_idx}")
        return slice(start, end_idx + 1)
