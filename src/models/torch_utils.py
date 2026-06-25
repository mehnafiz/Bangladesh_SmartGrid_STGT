"""Torch helpers for PF-STGT (does not modify Sprint 01 graph pipeline)."""

from __future__ import annotations

import torch
from torch import Tensor


def compute_attention_bias_torch(
    adjacency: Tensor,
    *,
    epsilon: float = 1e-6,
    mask_value: float = -1e9,
) -> Tensor:
    """Build additive attention bias tensor from adjacency."""
    if adjacency.dim() != 2 or adjacency.shape[0] != adjacency.shape[1]:
        raise ValueError("Adjacency must be a square 2D tensor")
    bias = torch.full(adjacency.shape, mask_value, dtype=adjacency.dtype, device=adjacency.device)
    positive = adjacency > 0
    bias[positive] = torch.log(adjacency[positive] + epsilon)
    return bias
