"""Temporal Transformer encoder (Phase 09)."""

from __future__ import annotations

import math

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor

from utils.logging import get_logger

logger = get_logger(__name__)


class TemporalMultiHeadAttention(nn.Module):
    """Multi-head self-attention over the temporal dimension."""

    def __init__(self, d_model: int, num_heads: int, dropout: float = 0.1) -> None:
        super().__init__()
        if d_model % num_heads != 0:
            raise ValueError("d_model must be divisible by num_heads")
        self.d_model = d_model
        self.num_heads = num_heads
        self.head_dim = d_model // num_heads
        self.scale = 1.0 / math.sqrt(self.head_dim)

        self.q_proj = nn.Linear(d_model, d_model)
        self.k_proj = nn.Linear(d_model, d_model)
        self.v_proj = nn.Linear(d_model, d_model)
        self.out_proj = nn.Linear(d_model, d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(
        self,
        x: Tensor,
        *,
        return_attention: bool = False,
    ) -> tuple[Tensor, Tensor | None]:
        """
        Args:
            x: (B, T, d_model)
        Returns:
            output (B, T, d_model), optional attn (B, H, T, T)
        """
        batch_size, timesteps, _ = x.shape
        q = self.q_proj(x).view(batch_size, timesteps, self.num_heads, self.head_dim)
        k = self.k_proj(x).view(batch_size, timesteps, self.num_heads, self.head_dim)
        v = self.v_proj(x).view(batch_size, timesteps, self.num_heads, self.head_dim)

        q = q.permute(0, 2, 1, 3)
        k = k.permute(0, 2, 1, 3)
        v = v.permute(0, 2, 1, 3)

        scores = torch.matmul(q, k.transpose(-2, -1)) * self.scale
        attn = F.softmax(scores, dim=-1)
        attn = self.dropout(attn)

        context = torch.matmul(attn, v)
        context = context.permute(0, 2, 1, 3).contiguous().view(batch_size, timesteps, self.d_model)
        output = self.out_proj(context)

        if return_attention:
            return output, attn
        return output, None


class TemporalTransformerLayer(nn.Module):
    """Single temporal Transformer encoder layer."""

    def __init__(
        self,
        d_model: int,
        num_heads: int,
        ffn_dim: int,
        dropout: float = 0.1,
    ) -> None:
        super().__init__()
        self.attn = TemporalMultiHeadAttention(d_model, num_heads, dropout)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.ffn = nn.Sequential(
            nn.Linear(d_model, ffn_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(ffn_dim, d_model),
            nn.Dropout(dropout),
        )

    def forward(
        self,
        x: Tensor,
        *,
        return_attention: bool = False,
    ) -> tuple[Tensor, Tensor | None]:
        attn_out, attn_weights = self.attn(
            self.norm1(x), return_attention=return_attention
        )
        x = x + attn_out
        x = x + self.ffn(self.norm2(x))
        return x, attn_weights


class TemporalTransformer(nn.Module):
    """
    Shared-weight temporal encoder applied per node.

    Input:  (B, T, N, d_model)
    Output: (B, T, N, d_model), optional temporal attention (B, H, T, T)
    """

    def __init__(
        self,
        d_model: int = 128,
        num_heads: int = 4,
        num_layers: int = 2,
        ffn_dim: int = 256,
        dropout: float = 0.1,
    ) -> None:
        super().__init__()
        self.layers = nn.ModuleList(
            [
                TemporalTransformerLayer(d_model, num_heads, ffn_dim, dropout)
                for _ in range(num_layers)
            ]
        )
        logger.debug(
            "TemporalTransformer initialized: layers=%s heads=%s d_model=%s",
            num_layers,
            num_heads,
            d_model,
        )

    def forward(
        self,
        x: Tensor,
        *,
        return_attention: bool = False,
    ) -> tuple[Tensor, Tensor | None]:
        batch_size, timesteps, n_nodes, d_model = x.shape
        flat = x.permute(0, 2, 1, 3).reshape(batch_size * n_nodes, timesteps, d_model)

        attn_weights: Tensor | None = None
        for layer_idx, layer in enumerate(self.layers):
            is_last = return_attention and layer_idx == len(self.layers) - 1
            flat, step_attn = layer(flat, return_attention=is_last)
            if is_last and step_attn is not None:
                heads, t1, t2 = step_attn.shape[1], step_attn.shape[2], step_attn.shape[3]
                step_attn = step_attn.view(batch_size, n_nodes, heads, t1, t2)
                attn_weights = step_attn.mean(dim=1)

        out = flat.view(batch_size, n_nodes, timesteps, d_model).permute(0, 2, 1, 3)
        return out, attn_weights
