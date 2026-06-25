"""Tests for trainer and validator with synthetic batches."""

from __future__ import annotations

import torch

from constants import GLOBAL_FEATURES, INPUT_WINDOW_T, N_NODES, NODE_FEATURES_PER_REGION
from models.pf_stgt import PFSTGT
from training.config import TrainingConfig
from training.trainer import Trainer
from training.validator import Validator


def _synthetic_batch(batch_size: int = 4) -> dict[str, torch.Tensor]:
    adj = torch.rand(N_NODES, N_NODES)
    adj = adj / adj.sum(dim=-1, keepdim=True).clamp_min(1e-6)
    adj.fill_diagonal_(0.0)
    return {
        "node_features": torch.randn(batch_size, INPUT_WINDOW_T, N_NODES, NODE_FEATURES_PER_REGION),
        "global_features": torch.randn(batch_size, INPUT_WINDOW_T, GLOBAL_FEATURES),
        "adjacency": adj,
        "attention_bias": torch.zeros(N_NODES, N_NODES),
        "demand_target": torch.abs(torch.randn(batch_size, N_NODES)) * 1000 + 500,
        "osi_target": torch.rand(batch_size, 1),
    }


def test_trainer_single_batch() -> None:
    config = TrainingConfig(batch_size=4, device="cpu")
    model = PFSTGT()
    trainer = Trainer(model, config)
    breakdown = trainer.train_batch(_synthetic_batch())
    assert breakdown.total >= 0.0


def test_validator_single_batch() -> None:
    config = TrainingConfig(batch_size=4, device="cpu")
    model = PFSTGT()
    trainer = Trainer(model, config)
    trainer.train_batch(_synthetic_batch())
    validator = Validator(model, config)
    from torch.utils.data import DataLoader, TensorDataset

    batch = _synthetic_batch(2)
    loader = DataLoader([batch], batch_size=1, collate_fn=lambda x: x[0])
    metrics = validator.validate(loader)
    assert metrics.demand.mae >= 0.0
    assert metrics.stress.mae >= 0.0
