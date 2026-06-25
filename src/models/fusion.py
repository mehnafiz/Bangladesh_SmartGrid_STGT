"""Parallel fusion module (Phase 09)."""

from __future__ import annotations

import torch
import torch.nn as nn
from torch import Tensor

from utils.logging import get_logger

logger = get_logger(__name__)


class ParallelFusion(nn.Module):
    """
    Gated parallel fusion of spatial and temporal branches.

    H_fused = gate * H_spatial + (1 - gate) * H_temporal
    gate = sigmoid(Linear([H_spatial; H_temporal]))
    """

    def __init__(self, d_model: int) -> None:
        super().__init__()
        self.gate_proj = nn.Linear(d_model * 2, d_model)
        self.sigmoid = nn.Sigmoid()
        logger.debug("ParallelFusion initialized with d_model=%s", d_model)

    def forward(self, h_spatial: Tensor, h_temporal: Tensor) -> Tensor:
        if h_spatial.shape != h_temporal.shape:
            raise ValueError(
                f"Branch shape mismatch: spatial {h_spatial.shape} vs temporal {h_temporal.shape}"
            )
        combined = torch.cat([h_spatial, h_temporal], dim=-1)
        gate = self.sigmoid(self.gate_proj(combined))
        fused = gate * h_spatial + (1.0 - gate) * h_temporal
        return fused

    @staticmethod
    def extract_shared(fused: Tensor) -> Tensor:
        """Take last-timestep representation: (B, T, N, d) -> (B, N, d)."""
        if fused.dim() != 4:
            raise ValueError(f"Expected 4D fused tensor, got shape {fused.shape}")
        return fused[:, -1, :, :]
