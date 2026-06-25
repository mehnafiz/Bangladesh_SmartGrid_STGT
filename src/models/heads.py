"""Multi-task prediction heads (Phase 09)."""

from __future__ import annotations

import torch
import torch.nn as nn
from torch import Tensor

from utils.logging import get_logger

logger = get_logger(__name__)


class DemandHead(nn.Module):
    """Per-node linear demand forecasting head."""

    def __init__(self, d_model: int, n_nodes: int = 9) -> None:
        super().__init__()
        self.n_nodes = n_nodes
        self.projection = nn.Linear(d_model, 1)

    def forward(self, h_shared: Tensor) -> Tensor:
        """
        Args:
            h_shared: (B, N, d_model)
        Returns:
            demand_pred: (B, N)
        """
        if h_shared.dim() != 3:
            raise ValueError(f"h_shared must be 3D, got {h_shared.shape}")
        preds = self.projection(h_shared).squeeze(-1)
        if preds.shape[-1] != self.n_nodes:
            raise ValueError(f"Expected {self.n_nodes} node outputs, got {preds.shape}")
        return preds


class StressHead(nn.Module):
    """
    Graph-level operational stress head.

    MLP([h_graph; flatten(H_shared)]) -> sigmoid -> OSI in [0, 1]
    """

    def __init__(
        self,
        d_model: int,
        n_nodes: int = 9,
        hidden_dim: int = 128,
    ) -> None:
        super().__init__()
        graph_dim = d_model * 2
        flat_dim = n_nodes * d_model
        input_dim = graph_dim + flat_dim
        self.mlp = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, 1),
        )
        logger.debug("StressHead input_dim=%s hidden_dim=%s", input_dim, hidden_dim)

    def forward(
        self,
        h_shared: Tensor,
        global_embedding: Tensor,
    ) -> Tensor:
        """
        Args:
            h_shared: (B, N, d_model)
            global_embedding: (B, d_model) from last-timestep global context
        Returns:
            osi_pred: (B, 1)
        """
        graph_mean = h_shared.mean(dim=1)
        h_graph = torch.cat([graph_mean, global_embedding], dim=-1)
        flat = h_shared.reshape(h_shared.shape[0], -1)
        features = torch.cat([h_graph, flat], dim=-1)
        return torch.sigmoid(self.mlp(features))
