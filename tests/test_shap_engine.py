"""Tests for SHAP engine."""

from __future__ import annotations

import torch

from constants import GLOBAL_FEATURES, INPUT_WINDOW_T, N_NODES, NODE_FEATURES_PER_REGION
from explainability.config import ExplainabilityConfig
from explainability.shap_engine import ShapEngine
from models.pf_stgt import PFSTGT


def _batch(batch_size: int = 1) -> dict[str, torch.Tensor]:
    adj = torch.rand(N_NODES, N_NODES)
    adj = adj / adj.sum(dim=-1, keepdim=True).clamp_min(1e-6)
    adj.fill_diagonal_(0.0)
    return {
        "node_features": torch.randn(
            batch_size, INPUT_WINDOW_T, N_NODES, NODE_FEATURES_PER_REGION
        ),
        "global_features": torch.randn(batch_size, INPUT_WINDOW_T, GLOBAL_FEATURES),
        "adjacency": adj,
        "attention_bias": torch.zeros(N_NODES, N_NODES),
    }


def test_local_demand_shap() -> None:
    config = ExplainabilityConfig(gradient_shap_steps=5, device="cpu")
    engine = ShapEngine(PFSTGT(), config)
    result = engine.explain_local(_batch(), task="demand", region_index=3)
    assert len(result.grouped.group_ids) == 10
    assert result.grouped.phi.shape == (10,)
    assert result.node_attributions is not None


def test_local_stress_shap() -> None:
    config = ExplainabilityConfig(gradient_shap_steps=5, device="cpu")
    engine = ShapEngine(PFSTGT(), config)
    result = engine.explain_local(_batch(), task="stress")
    assert len(result.grouped.group_ids) == 8
    assert "G11" in result.grouped.group_ids


def test_rank_groups() -> None:
    config = ExplainabilityConfig(gradient_shap_steps=3, device="cpu")
    engine = ShapEngine(PFSTGT(), config)
    result = engine.explain_local(_batch(), task="stress")
    ranking = engine.rank_groups(result.grouped)
    assert len(ranking) == len(result.grouped.group_ids)
