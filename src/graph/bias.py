"""Attention bias construction from adjacency."""

from __future__ import annotations

import numpy as np

from utils.exceptions import GraphValidationError


def compute_attention_bias(
    adjacency: np.ndarray,
    *,
    epsilon: float = 1e-6,
    mask_value: float = -1e9,
) -> np.ndarray:
    """
    Build additive attention bias: log(A_ij + eps) where A_ij > 0 else mask_value.

    Matches Phase 09 Graph Transformer specification.
    """
    if adjacency.ndim != 2 or adjacency.shape[0] != adjacency.shape[1]:
        raise GraphValidationError("Adjacency must be a square matrix")

    bias = np.full(adjacency.shape, mask_value, dtype=np.float32)
    positive = adjacency > 0
    bias[positive] = np.log(adjacency[positive] + epsilon).astype(np.float32)
    return bias


class AdjacencyBias:
    """Callable wrapper for attention bias generation."""

    def __init__(self, epsilon: float = 1e-6, mask_value: float = -1e9) -> None:
        self.epsilon = epsilon
        self.mask_value = mask_value

    def build(self, adjacency: np.ndarray) -> np.ndarray:
        return compute_attention_bias(
            adjacency,
            epsilon=self.epsilon,
            mask_value=self.mask_value,
        )
