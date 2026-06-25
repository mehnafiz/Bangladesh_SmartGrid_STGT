"""Temporal tensor datatypes."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class TemporalBatch:
    """Single-sample temporal tensors (X_temporal components)."""

    node_features: np.ndarray
    global_features: np.ndarray
    end_idx: int

    @property
    def shape_node(self) -> tuple[int, int, int]:
        return self.node_features.shape

    @property
    def shape_global(self) -> tuple[int, int]:
        return self.global_features.shape


@dataclass(frozen=True)
class XTemporal:
    """Sprint 01 output alias for temporal input tensors."""

    node_features: np.ndarray
    global_features: np.ndarray

    @classmethod
    def from_batch(cls, batch: TemporalBatch) -> XTemporal:
        return cls(
            node_features=batch.node_features,
            global_features=batch.global_features,
        )
