"""Tests for attention extraction."""

from __future__ import annotations

import numpy as np
import torch

from explainability.attention_extractor import AttentionExtractor
from constants import INPUT_WINDOW_T, N_NODES


def test_spatial_influence_matrix() -> None:
    attn = torch.rand(2, 4, N_NODES, N_NODES)
    attn = attn / attn.sum(dim=-1, keepdim=True)
    adj = torch.rand(N_NODES, N_NODES)
    result = AttentionExtractor().extract_spatial(attn, adjacency=adj)
    assert result.influence_matrix.shape == (N_NODES, N_NODES)
    assert np.isfinite(result.influence_matrix).all()


def test_temporal_alpha_normalised() -> None:
    attn = torch.rand(2, 4, INPUT_WINDOW_T, INPUT_WINDOW_T)
    attn = attn / attn.sum(dim=-1, keepdim=True)
    result = AttentionExtractor().extract_temporal(attn)
    assert result.alpha_t.shape == (INPUT_WINDOW_T,)
    assert abs(result.alpha_t.sum() - 1.0) < 1e-5


def test_spearman_with_adjacency() -> None:
    extractor = AttentionExtractor()
    adj = np.eye(N_NODES)
    adj[0, 1] = 0.8
    adj[1, 0] = 0.8
    influence = adj.copy()
    rho = extractor.spearman_with_adjacency(influence, adj)
    assert -1.0 <= rho <= 1.0
