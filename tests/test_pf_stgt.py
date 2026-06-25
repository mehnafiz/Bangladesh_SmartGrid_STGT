"""Tests for PF-STGT core model."""

from __future__ import annotations

import pytest
import torch

from constants import GLOBAL_FEATURES, INPUT_WINDOW_T, N_NODES, NODE_FEATURES_PER_REGION
from models.config import PFSTGTConfig
from models.pf_stgt import PFSTGT
from models.types import validate_input_shapes, validate_output_shapes


@pytest.fixture
def cfg() -> PFSTGTConfig:
    return PFSTGTConfig()


@pytest.fixture
def model(cfg: PFSTGTConfig) -> PFSTGT:
    return PFSTGT(cfg)


@pytest.fixture
def dummy_batch(cfg: PFSTGTConfig) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    batch_size = 4
    node = torch.randn(batch_size, cfg.input_window_t, cfg.n_nodes, cfg.node_features)
    global_ = torch.randn(batch_size, cfg.input_window_t, cfg.global_features)
    adjacency = torch.rand(cfg.n_nodes, cfg.n_nodes)
    adjacency = adjacency / adjacency.sum(dim=-1, keepdim=True).clamp_min(1e-6)
    torch.diagonal(adjacency).zero_()
    return node, global_, adjacency


def test_forward_pass(model: PFSTGT, dummy_batch) -> None:
    node, global_, adj = dummy_batch
    output = model(node, global_, adj, return_attention=True)
    assert output.demand_pred.shape == (4, N_NODES)
    assert output.osi_pred.shape == (4, 1)
    assert torch.isfinite(output.demand_pred).all()
    assert torch.isfinite(output.osi_pred).all()
    assert (output.osi_pred >= 0.0).all() and (output.osi_pred <= 1.0).all()


def test_input_shape_validation(cfg: PFSTGTConfig) -> None:
    node = torch.randn(2, INPUT_WINDOW_T, N_NODES, NODE_FEATURES_PER_REGION)
    global_ = torch.randn(2, INPUT_WINDOW_T, GLOBAL_FEATURES)
    adj = torch.eye(N_NODES)
    batch_size = validate_input_shapes(node, global_, adj, cfg=cfg)
    assert batch_size == 2


def test_input_shape_validation_rejects_bad_shapes(cfg: PFSTGTConfig) -> None:
    node = torch.randn(2, 5, N_NODES, NODE_FEATURES_PER_REGION)
    global_ = torch.randn(2, INPUT_WINDOW_T, GLOBAL_FEATURES)
    adj = torch.eye(N_NODES)
    with pytest.raises(ValueError, match="node_features"):
        validate_input_shapes(node, global_, adj, cfg=cfg)


def test_output_shape_validation() -> None:
    demand = torch.randn(3, N_NODES)
    osi = torch.randn(3, 1)
    validate_output_shapes(demand, osi, batch_size=3)


def test_single_sample_unbatched(model: PFSTGT, cfg: PFSTGTConfig) -> None:
    node = torch.randn(cfg.input_window_t, cfg.n_nodes, cfg.node_features)
    global_ = torch.randn(cfg.input_window_t, cfg.global_features)
    adj = torch.rand(cfg.n_nodes, cfg.n_nodes)
    adj = adj / adj.sum(dim=-1, keepdim=True).clamp_min(1e-6)
    torch.diagonal(adj).zero_()
    output = model(node, global_, adj)
    assert output.demand_pred.shape == (1, N_NODES)
    assert output.osi_pred.shape == (1, 1)


def test_attention_export_shapes(model: PFSTGT, dummy_batch, cfg: PFSTGTConfig) -> None:
    node, global_, adj = dummy_batch
    output = model(node, global_, adj, return_attention=True)
    assert output.attn_spatial is not None
    assert output.attn_temporal is not None
    assert output.attn_spatial.shape == (4, cfg.num_heads, N_NODES, N_NODES)
    assert output.attn_temporal.shape == (4, cfg.num_heads, INPUT_WINDOW_T, INPUT_WINDOW_T)


def test_parameter_count(model: PFSTGT) -> None:
    count = model.count_parameters()
    assert 500_000 <= count <= 2_000_000
