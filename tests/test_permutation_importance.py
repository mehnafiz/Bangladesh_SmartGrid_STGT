"""Tests for permutation importance."""

from __future__ import annotations

import torch
from torch.utils.data import DataLoader

from constants import GLOBAL_FEATURES, INPUT_WINDOW_T, N_NODES, NODE_FEATURES_PER_REGION
from explainability.config import ExplainabilityConfig
from explainability.permutation import PermutationImportance
from models.pf_stgt import PFSTGT


def _batch(batch_size: int = 4) -> dict[str, torch.Tensor]:
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
        "demand_target": torch.abs(torch.randn(batch_size, N_NODES)) * 1000,
        "osi_target": torch.rand(batch_size, 1),
    }


def test_permutation_importance_demand() -> None:
    config = ExplainabilityConfig(permutation_repeats=2, device="cpu")
    model = PFSTGT()
    pi = PermutationImportance(model, config)
    loader = DataLoader([_batch()], batch_size=1, collate_fn=lambda x: x[0])
    result = pi.compute(loader, task="demand", max_batches=1, n_repeats=2)
    assert len(result.entries) == 10
    assert result.baseline_score >= 0.0


def test_spearman_vs_shap() -> None:
    config = ExplainabilityConfig(device="cpu")
    pi = PermutationImportance(PFSTGT(), config)
    from explainability.types import PermutationImportanceEntry, PermutationImportanceResult

    entries = tuple(
        PermutationImportanceEntry(group_id=f"G{i}", mean_delta=float(i), std_delta=0.0)
        for i in range(1, 4)
    )
    result = PermutationImportanceResult(task="stress", entries=entries, baseline_score=1.0)
    rho = pi.spearman_vs_shap(result, grouped_shap=[3.0, 2.0, 1.0], group_ids=("G1", "G2", "G3"))
    assert -1.0 <= rho <= 1.0
