"""Graph tensor datatypes."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from constants import N_NODES


@dataclass(frozen=True)
class XGraph:
    """Sprint 01 graph output tensors."""

    adjacency: np.ndarray
    attention_bias: np.ndarray
    variant: str

    def __post_init__(self) -> None:
        if self.adjacency.shape != (N_NODES, N_NODES):
            raise ValueError(f"Adjacency shape must be ({N_NODES}, {N_NODES})")
        if self.attention_bias.shape != (N_NODES, N_NODES):
            raise ValueError(f"Bias shape must be ({N_NODES}, {N_NODES})")
