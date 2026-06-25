"""Spatial and temporal attention extraction (Phase 12 L3/L4)."""

from __future__ import annotations

import numpy as np
import torch
from torch import Tensor

from explainability.types import SpatialAttentionResult, TemporalAttentionResult
from utils.logging import get_logger

logger = get_logger(__name__)


class AttentionExtractor:
    """
    Extract and aggregate PF-STGT attention maps.

    Spatial attention is exported from the final graph-transformer layer at the
    last lookback timestep (model contract from Sprint 02).
    Temporal attention is averaged across nodes after the final temporal layer.
    """

    def extract_spatial(
        self,
        attn_spatial: Tensor,
        *,
        adjacency: Tensor | np.ndarray | None = None,
    ) -> SpatialAttentionResult:
        """
        Aggregate spatial attention to an inter-regional influence matrix.

        Args:
            attn_spatial: (B, H, N, N) or (H, N, N)
            adjacency: optional (N, N) hybrid graph for edge masking
        """
        weights = self._to_numpy(attn_spatial)
        if weights.ndim == 4:
            influence = weights.mean(axis=(0, 1))
            per_head = weights.mean(axis=0)
        elif weights.ndim == 3:
            influence = weights.mean(axis=0)
            per_head = weights
        else:
            raise ValueError(f"Unexpected spatial attention shape: {weights.shape}")

        if adjacency is not None:
            adj = self._to_numpy(adjacency)
            edge_mask = adj > 0
            influence = np.where(edge_mask, influence, 0.0)

        logger.debug(
            "Extracted spatial attention influence matrix shape=%s",
            influence.shape,
        )
        return SpatialAttentionResult(influence_matrix=influence, per_head=per_head)

    def extract_temporal(self, attn_temporal: Tensor) -> TemporalAttentionResult:
        """
        Aggregate temporal attention to α_t contributions.

        α_t = mean_{heads, query positions}( attn[:, :, t] )
        """
        weights = self._to_numpy(attn_temporal)
        if weights.ndim == 4:
            alpha_t = weights.mean(axis=(0, 1, 2))
            per_head = weights.mean(axis=(0, 2))
        elif weights.ndim == 3:
            alpha_t = weights.mean(axis=(0, 1))
            per_head = weights.mean(axis=1)
        else:
            raise ValueError(f"Unexpected temporal attention shape: {weights.shape}")

        alpha_t = alpha_t / np.clip(alpha_t.sum(), 1e-8, None)
        logger.debug("Extracted temporal attribution alpha_t shape=%s", alpha_t.shape)
        return TemporalAttentionResult(alpha_t=alpha_t, per_head=per_head)

    def spatial_inflow_outflow(
        self,
        influence_matrix: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray]:
        """Return per-node incoming and outgoing attention mass."""
        inflow = influence_matrix.sum(axis=0)
        outflow = influence_matrix.sum(axis=1)
        return inflow, outflow

    def spearman_with_adjacency(
        self,
        influence_matrix: np.ndarray,
        adjacency: np.ndarray,
    ) -> float:
        """Spearman ρ between learned attention and hybrid edge weights on edges."""
        from scipy.stats import spearmanr

        edge_mask = adjacency > 0
        if edge_mask.sum() < 2:
            return 0.0
        rho, _ = spearmanr(
            influence_matrix[edge_mask].ravel(),
            adjacency[edge_mask].ravel(),
        )
        if np.isnan(rho):
            return 0.0
        return float(rho)

    @staticmethod
    def _to_numpy(value: Tensor | np.ndarray) -> np.ndarray:
        if isinstance(value, Tensor):
            return value.detach().cpu().numpy()
        return np.asarray(value)
