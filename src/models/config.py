"""PF-STGT model configuration (Phase 09 / Phase 11 defaults)."""

from __future__ import annotations

from dataclasses import dataclass

from constants import (
    GLOBAL_FEATURES,
    INPUT_WINDOW_T,
    N_NODES,
    NODE_FEATURES_PER_REGION,
)


@dataclass(frozen=True)
class PFSTGTConfig:
    """Frozen default hyperparameters for PF-STGT."""

    input_window_t: int = INPUT_WINDOW_T
    n_nodes: int = N_NODES
    node_features: int = NODE_FEATURES_PER_REGION
    global_features: int = GLOBAL_FEATURES
    d_model: int = 128
    num_heads: int = 4
    num_spatial_layers: int = 2
    num_temporal_layers: int = 2
    ffn_dim: int = 256
    spatial_dropout: float = 0.1
    temporal_dropout: float = 0.1
    stress_hidden_dim: int = 128

    def __post_init__(self) -> None:
        if self.d_model % self.num_heads != 0:
            raise ValueError(
                f"d_model ({self.d_model}) must be divisible by num_heads ({self.num_heads})"
            )
