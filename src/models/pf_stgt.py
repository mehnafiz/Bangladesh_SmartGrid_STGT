"""PF-STGT — Parallel-Fusion Spatio-Temporal Graph Transformer."""

from __future__ import annotations

import torch
import torch.nn as nn
from torch import Tensor

from models.torch_utils import compute_attention_bias_torch
from models.config import PFSTGTConfig
from models.fusion import ParallelFusion
from models.graph_transformer import GraphTransformer
from models.heads import DemandHead, StressHead
from models.temporal_transformer import TemporalTransformer
from models.types import ModelOutput, validate_input_shapes
from utils.logging import get_logger

logger = get_logger(__name__)


class InputEmbedding(nn.Module):
    """
    Project node/global features into shared d_model space.

    H0 = E_node + broadcast(E_global) + PosEnc_time(T)
    """

    def __init__(self, cfg: PFSTGTConfig) -> None:
        super().__init__()
        self.cfg = cfg
        self.node_proj = nn.Linear(cfg.node_features, cfg.d_model)
        self.global_proj = nn.Linear(cfg.global_features, cfg.d_model)
        self.region_embedding = nn.Embedding(cfg.n_nodes, cfg.d_model)
        self.positional = nn.Parameter(
            torch.zeros(1, cfg.input_window_t, 1, cfg.d_model)
        )
        nn.init.trunc_normal_(self.positional, std=0.02)

    def forward(self, node_features: Tensor, global_features: Tensor) -> tuple[Tensor, Tensor]:
        batch_size = node_features.shape[0]
        node_emb = self.node_proj(node_features)
        region_ids = torch.arange(self.cfg.n_nodes, device=node_features.device)
        node_emb = node_emb + self.region_embedding(region_ids).view(1, 1, self.cfg.n_nodes, self.cfg.d_model)

        global_emb = self.global_proj(global_features)
        global_emb = global_emb.unsqueeze(2)
        h0 = node_emb + global_emb + self.positional

        last_global = global_emb[:, -1, 0, :]
        return h0, last_global


class PFSTGT(nn.Module):
    """
    Parallel-Fusion Spatio-Temporal Graph Transformer (Phase 09).

    Inputs:
        node_features: (B, T, N, F_n)
        global_features: (B, T, F_g)
        adjacency: (N, N) row-normalised hybrid graph
        attention_bias: optional (N, N); computed from adjacency if omitted

    Outputs:
        demand_pred: (B, N)
        osi_pred: (B, 1)
    """

    def __init__(self, cfg: PFSTGTConfig | None = None) -> None:
        super().__init__()
        self.cfg = cfg or PFSTGTConfig()
        self.embedding = InputEmbedding(self.cfg)
        self.graph_transformer = GraphTransformer(
            d_model=self.cfg.d_model,
            num_heads=self.cfg.num_heads,
            num_layers=self.cfg.num_spatial_layers,
            ffn_dim=self.cfg.ffn_dim,
            dropout=self.cfg.spatial_dropout,
        )
        self.temporal_transformer = TemporalTransformer(
            d_model=self.cfg.d_model,
            num_heads=self.cfg.num_heads,
            num_layers=self.cfg.num_temporal_layers,
            ffn_dim=self.cfg.ffn_dim,
            dropout=self.cfg.temporal_dropout,
        )
        self.fusion = ParallelFusion(self.cfg.d_model)
        self.demand_head = DemandHead(self.cfg.d_model, self.cfg.n_nodes)
        self.stress_head = StressHead(
            self.cfg.d_model,
            self.cfg.n_nodes,
            hidden_dim=self.cfg.stress_hidden_dim,
        )
        param_count = sum(p.numel() for p in self.parameters())
        logger.info("PFSTGT initialized with %s parameters", f"{param_count:,}")

    def forward(
        self,
        node_features: Tensor,
        global_features: Tensor,
        adjacency: Tensor,
        *,
        attention_bias: Tensor | None = None,
        return_attention: bool = False,
    ) -> ModelOutput:
        if node_features.dim() == 3:
            node_features = node_features.unsqueeze(0)
        if global_features.dim() == 2:
            global_features = global_features.unsqueeze(0)

        batch_size = validate_input_shapes(
            node_features, global_features, adjacency, cfg=self.cfg
        )

        if attention_bias is None:
            attention_bias = compute_attention_bias_torch(
                adjacency.to(dtype=node_features.dtype, device=node_features.device)
            )
        else:
            attention_bias = attention_bias.to(
                dtype=node_features.dtype, device=node_features.device
            )

        h0, last_global = self.embedding(node_features, global_features)

        h_spatial, attn_spatial = self.graph_transformer(
            h0,
            attention_bias,
            return_attention=return_attention,
        )
        h_temporal, attn_temporal = self.temporal_transformer(
            h0,
            return_attention=return_attention,
        )

        h_fused = self.fusion(h_spatial, h_temporal)
        h_shared = ParallelFusion.extract_shared(h_fused)

        demand_pred = self.demand_head(h_shared)
        osi_pred = self.stress_head(h_shared, last_global)

        output = ModelOutput(
            demand_pred=demand_pred,
            osi_pred=osi_pred,
            attn_spatial=attn_spatial,
            attn_temporal=attn_temporal,
            h_shared=h_shared,
        )
        output.validate(batch_size, self.cfg)
        return output

    def count_parameters(self, trainable_only: bool = True) -> int:
        if trainable_only:
            return sum(p.numel() for p in self.parameters() if p.requires_grad)
        return sum(p.numel() for p in self.parameters())
