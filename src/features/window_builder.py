"""Temporal window construction."""

from __future__ import annotations

import pandas as pd

from constants import GLOBAL_FEATURES, INPUT_WINDOW_T, N_NODES, NODE_FEATURES_PER_REGION
from data.splits import SplitManager
from features.global_features import GlobalFeatureBuilder
from features.node_features import NodeFeatureBuilder
from features.temporal import TemporalBatch
from utils.exceptions import FeatureValidationError


class WindowBuilder:
    """Build T-step windows ending at a given index."""

    def __init__(
        self,
        window_size: int = INPUT_WINDOW_T,
        split_manager: SplitManager | None = None,
    ) -> None:
        self.window_size = window_size
        self.split_manager = split_manager or SplitManager(window_size=window_size)
        self.node_builder = NodeFeatureBuilder()
        self.global_builder = GlobalFeatureBuilder()

    def build(self, features: pd.DataFrame, end_idx: int) -> TemporalBatch:
        window_slice = self.split_manager.window_slice(end_idx)
        frame = features.iloc[window_slice]
        if len(frame) != self.window_size:
            raise FeatureValidationError(
                f"Window length {len(frame)} != expected {self.window_size}"
            )

        node = self.node_builder.build_frame(frame)
        global_ = self.global_builder.build_frame(frame)

        if node.shape != (self.window_size, N_NODES, NODE_FEATURES_PER_REGION):
            raise FeatureValidationError(f"Unexpected node tensor shape: {node.shape}")
        if global_.shape != (self.window_size, GLOBAL_FEATURES):
            raise FeatureValidationError(f"Unexpected global tensor shape: {global_.shape}")

        return TemporalBatch(
            node_features=node,
            global_features=global_,
            end_idx=end_idx,
        )
