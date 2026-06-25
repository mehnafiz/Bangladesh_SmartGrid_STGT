"""P2 feature pipeline orchestrator."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from features.leakage_guard import assert_no_osi_in_inputs
from features.specs import GLOBAL_INPUT_FEATURE_NAMES
from features.temporal import TemporalBatch, XTemporal
from features.window_builder import WindowBuilder
from utils.logging import get_logger

logger = get_logger(__name__)


@dataclass(frozen=True)
class FeaturePipelineResult:
    batch: TemporalBatch
    x_temporal: XTemporal


class FeaturePipeline:
    """Construct temporal tensors from a feature dataframe."""

    def __init__(self, window_builder: WindowBuilder | None = None) -> None:
        self.window_builder = window_builder or WindowBuilder()
        assert_no_osi_in_inputs(list(GLOBAL_INPUT_FEATURE_NAMES))

    def build_sample(self, features: pd.DataFrame, end_idx: int) -> FeaturePipelineResult:
        batch = self.window_builder.build(features, end_idx)
        x_temporal = XTemporal.from_batch(batch)
        logger.debug(
            "Built X_temporal at end_idx=%s shapes node=%s global=%s",
            end_idx,
            x_temporal.node_features.shape,
            x_temporal.global_features.shape,
        )
        return FeaturePipelineResult(batch=batch, x_temporal=x_temporal)
