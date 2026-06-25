"""Benchmark model definitions for Experiment 02 (experiment-local only)."""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor


class SequenceRegressor(nn.Module):
    """Shared LSTM/GRU trunk for B04/B05."""

    def __init__(
        self,
        input_dim: int,
        hidden_dim: int = 128,
        *,
        cell: str = "lstm",
        num_layers: int = 2,
        n_regions: int = 9,
    ) -> None:
        super().__init__()
        self.cell_type = cell
        rnn_cls = nn.LSTM if cell == "lstm" else nn.GRU
        self.rnn = rnn_cls(
            input_dim,
            hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            dropout=0.1 if num_layers > 1 else 0.0,
        )
        self.demand_head = nn.Linear(hidden_dim, n_regions)
        self.stress_head = nn.Sequential(
            nn.Linear(hidden_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Sigmoid(),
        )

    def forward(self, x: Tensor) -> tuple[Tensor, Tensor]:
        out, _ = self.rnn(x)
        last = out[:, -1, :]
        return self.demand_head(last), self.stress_head(last)


class GraphConvLayer(nn.Module):
    """Single-hop graph convolution with row-normalised adjacency."""

    def forward(self, x: Tensor, adjacency: Tensor) -> Tensor:
        # x: (B, N, F), adjacency: (N, N)
        return torch.einsum("ij,bjf->bif", adjacency, x)


class TGCN(nn.Module):
    """Minimal spatio-temporal GCN baseline (B06)."""

    def __init__(
        self,
        node_features: int,
        global_features: int,
        hidden_dim: int = 64,
        n_regions: int = 9,
    ) -> None:
        super().__init__()
        self.node_proj = nn.Linear(node_features, hidden_dim)
        self.global_proj = nn.Linear(global_features, hidden_dim)
        self.temporal = nn.GRU(hidden_dim, hidden_dim, batch_first=True)
        self.demand_head = nn.Linear(hidden_dim, n_regions)
        self.stress_head = nn.Sequential(
            nn.Linear(hidden_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Sigmoid(),
        )

    def forward(
        self,
        node_features: Tensor,
        global_features: Tensor,
        adjacency: Tensor,
    ) -> tuple[Tensor, Tensor]:
        batch_size, timesteps, n_nodes, _ = node_features.shape
        seq: list[Tensor] = []
        for t in range(timesteps):
            h = self.node_proj(node_features[:, t])
            h = torch.einsum("ij,bjf->bif", adjacency, h)
            g = self.global_proj(global_features[:, t]).unsqueeze(1)
            seq.append((h + g).mean(dim=1))
        stacked = torch.stack(seq, dim=1)
        out, _ = self.temporal(stacked)
        last = out[:, -1, :]
        return self.demand_head(last), self.stress_head(last)
