"""Graph Transformer spatial encoder (Phase 09)."""

from __future__ import annotations

import math

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor

from utils.logging import get_logger

logger = get_logger(__name__)


class GraphMultiHeadAttention(nn.Module):
    """Multi-head self-attention over graph nodes with adjacency bias."""

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
        adjacency_bias: Tensor,
        *,
        return_attention: bool = False,
    ) -> tuple[Tensor, Tensor | None]:
        """
        Args:
            x: (B, N, d_model)
            adjacency_bias: (N, N) additive attention bias
        Returns:
            output (B, N, d_model), optional attn weights (B, H, N, N)
        """
        batch_size, n_nodes, _ = x.shape
        q = self.q_proj(x).view(batch_size, n_nodes, self.num_heads, self.head_dim)
        k = self.k_proj(x).view(batch_size, n_nodes, self.num_heads, self.head_dim)
        v = self.v_proj(x).view(batch_size, n_nodes, self.num_heads, self.head_dim)

        q = q.permute(0, 2, 1, 3)
        k = k.permute(0, 2, 1, 3)
        v = v.permute(0, 2, 1, 3)

        scores = torch.matmul(q, k.transpose(-2, -1)) * self.scale
        scores = scores + adjacency_bias.unsqueeze(0).unsqueeze(0)
        attn = F.softmax(scores, dim=-1)
        attn = self.dropout(attn)

        context = torch.matmul(attn, v)
        context = context.permute(0, 2, 1, 3).contiguous().view(batch_size, n_nodes, self.d_model)
        output = self.out_proj(context)

        if return_attention:
            return output, attn
        return output, None


class GraphTransformerLayer(nn.Module):
    """Single Graph Transformer encoder layer."""

    def __init__(
        self,
        d_model: int,
        num_heads: int,
        ffn_dim: int,
        dropout: float = 0.1,
    ) -> None:
        super().__init__()
        self.attn = GraphMultiHeadAttention(d_model, num_heads, dropout)
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
        adjacency_bias: Tensor,
        *,
        return_attention: bool = False,
    ) -> tuple[Tensor, Tensor | None]:
        attn_out, attn_weights = self.attn(
            self.norm1(x), adjacency_bias, return_attention=return_attention
        )
        x = x + attn_out
        x = x + self.ffn(self.norm2(x))
        return x, attn_weights


class GraphTransformer(nn.Module):
    """
    Apply graph self-attention at each timestep.

    Input:  (B, T, N, d_model)
    Output: (B, T, N, d_model), optional spatial attention from final layer (B, H, N, N)
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
                GraphTransformerLayer(d_model, num_heads, ffn_dim, dropout)
                for _ in range(num_layers)
            ]
        )
        logger.debug(
            "GraphTransformer initialized: layers=%s heads=%s d_model=%s",
            num_layers,
            num_heads,
            d_model,
        )

    def forward(
        self,
        x: Tensor,
        adjacency_bias: Tensor,
        *,
        return_attention: bool = False,
    ) -> tuple[Tensor, Tensor | None]:
        batch_size, timesteps, n_nodes, d_model = x.shape
        out = x
        attn_weights: Tensor | None = None

        for layer_idx, layer in enumerate(self.layers):
            timestep_outputs: list[Tensor] = []
            last_step_attn: Tensor | None = None
            for t in range(timesteps):
                step_x = out[:, t, :, :]
                is_last = return_attention and layer_idx == len(self.layers) - 1
                step_out, step_attn = layer(
                    step_x,
                    adjacency_bias,
                    return_attention=is_last,
                )
                timestep_outputs.append(step_out)
                if is_last:
                    last_step_attn = step_attn
            out = torch.stack(timestep_outputs, dim=1)
            attn_weights = last_step_attn

        return out, attn_weights
