"""Experiment 03 ablation variants (experiment-local, no sprint changes)."""

from __future__ import annotations

import torch
import torch.nn as nn
from torch import Tensor

from models.config import PFSTGTConfig
from models.fusion import ParallelFusion
from models.pf_stgt import PFSTGT
from models.torch_utils import compute_attention_bias_torch
from models.types import ModelOutput, validate_input_shapes


class AblationPFSTGT(nn.Module):
    """
    PF-STGT with structural ablation switches (A2–A4).

    A1 / A5 / A6 use full PFSTGT with graph variant chosen at data layer.
    """

    def __init__(self, ablation_id: str, cfg: PFSTGTConfig | None = None) -> None:
        super().__init__()
        self.ablation_id = ablation_id
        self.model = PFSTGT(cfg)

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
            node_features, global_features, adjacency, cfg=self.model.cfg
        )

        if attention_bias is None:
            attention_bias = compute_attention_bias_torch(
                adjacency.to(dtype=node_features.dtype, device=node_features.device)
            )
        else:
            attention_bias = attention_bias.to(
                dtype=node_features.dtype, device=node_features.device
            )

        h0, last_global = self.model.embedding(node_features, global_features)

        if self.ablation_id == "A2":
            h_temporal, attn_temporal = self.model.temporal_transformer(
                h0, return_attention=return_attention
            )
            h_shared = ParallelFusion.extract_shared(h_temporal)
            attn_spatial = None
        elif self.ablation_id == "A3":
            h_spatial, attn_spatial = self.model.graph_transformer(
                h0, attention_bias, return_attention=return_attention
            )
            h_shared = ParallelFusion.extract_shared(h_spatial)
            attn_temporal = None
        else:
            h_spatial, attn_spatial = self.model.graph_transformer(
                h0, attention_bias, return_attention=return_attention
            )
            h_temporal, attn_temporal = self.model.temporal_transformer(
                h0, return_attention=return_attention
            )
            h_fused = self.model.fusion(h_spatial, h_temporal)
            h_shared = ParallelFusion.extract_shared(h_fused)

        demand_pred = self.model.demand_head(h_shared)

        if self.ablation_id == "A4":
            osi_pred = torch.zeros(batch_size, 1, device=node_features.device, dtype=node_features.dtype)
        else:
            osi_pred = self.model.stress_head(h_shared, last_global)

        output = ModelOutput(
            demand_pred=demand_pred,
            osi_pred=osi_pred,
            attn_spatial=attn_spatial if self.ablation_id != "A2" else None,
            attn_temporal=attn_temporal if self.ablation_id != "A3" else None,
            h_shared=h_shared,
        )
        output.validate(batch_size, self.model.cfg)
        return output

    def load_full_state_dict(self, state_dict: dict[str, Tensor]) -> None:
        self.model.load_state_dict(state_dict)
