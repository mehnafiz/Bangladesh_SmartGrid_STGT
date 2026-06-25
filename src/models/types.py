"""PF-STGT input/output types and shape validation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import torch
from torch import Tensor

from constants import GLOBAL_FEATURES, INPUT_WINDOW_T, N_NODES, NODE_FEATURES_PER_REGION
from models.config import PFSTGTConfig


@dataclass
class ModelOutput:
    """Forward pass outputs for PF-STGT."""

    demand_pred: Tensor
    osi_pred: Tensor
    attn_spatial: Tensor | None = None
    attn_temporal: Tensor | None = None
    h_shared: Tensor | None = None

    def validate(self, batch_size: int, cfg: PFSTGTConfig | None = None) -> None:
        cfg = cfg or PFSTGTConfig()
        validate_output_shapes(
            self.demand_pred,
            self.osi_pred,
            batch_size=batch_size,
            n_nodes=cfg.n_nodes,
        )


def validate_input_shapes(
    node_features: Tensor,
    global_features: Tensor,
    adjacency: Tensor,
    *,
    cfg: PFSTGTConfig | None = None,
) -> int:
    """Validate model inputs; return batch size."""
    cfg = cfg or PFSTGTConfig()

    if node_features.dim() not in (3, 4):
        raise ValueError(f"node_features must be 3D or 4D, got {node_features.dim()}D")
    if global_features.dim() not in (2, 3):
        raise ValueError(f"global_features must be 2D or 3D, got {global_features.dim()}D")

    if node_features.dim() == 3:
        node_features = node_features.unsqueeze(0)
    if global_features.dim() == 2:
        global_features = global_features.unsqueeze(0)

    batch_size = node_features.shape[0]
    expected_node = (
        batch_size,
        cfg.input_window_t,
        cfg.n_nodes,
        cfg.node_features,
    )
    expected_global = (batch_size, cfg.input_window_t, cfg.global_features)
    expected_adj = (cfg.n_nodes, cfg.n_nodes)

    if tuple(node_features.shape) != expected_node:
        raise ValueError(
            f"node_features expected {expected_node}, got {tuple(node_features.shape)}"
        )
    if tuple(global_features.shape) != expected_global:
        raise ValueError(
            f"global_features expected {expected_global}, got {tuple(global_features.shape)}"
        )
    if tuple(adjacency.shape) != expected_adj:
        raise ValueError(f"adjacency expected {expected_adj}, got {tuple(adjacency.shape)}")

    return batch_size


def validate_output_shapes(
    demand_pred: Tensor,
    osi_pred: Tensor,
    *,
    batch_size: int,
    n_nodes: int = N_NODES,
) -> None:
    """Validate demand and OSI prediction shapes."""
    if demand_pred.dim() == 1:
        demand_pred = demand_pred.unsqueeze(0)
    if osi_pred.dim() == 1:
        osi_pred = osi_pred.unsqueeze(0)

    if tuple(demand_pred.shape) != (batch_size, n_nodes):
        raise ValueError(
            f"demand_pred expected ({batch_size}, {n_nodes}), got {tuple(demand_pred.shape)}"
        )

    if osi_pred.shape[0] != batch_size:
        raise ValueError(f"osi_pred batch mismatch: {osi_pred.shape[0]} vs {batch_size}")
    if osi_pred.shape[-1] != 1:
        raise ValueError(f"osi_pred last dim must be 1, got {osi_pred.shape}")
