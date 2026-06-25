"""Integration test: PF-STGT forward on Sprint 01 foundation sample."""

from __future__ import annotations

import numpy as np
import pytest
import torch

from constants import GLOBAL_FEATURES, INPUT_WINDOW_T, N_NODES, NODE_FEATURES_PER_REGION
from foundation import FoundationCoordinator
from models.pf_stgt import PFSTGT


@pytest.fixture(scope="module")
def foundation_sample():
    coordinator = FoundationCoordinator(verify_md5=True)
    return coordinator.smoke_sample("train")


def test_pf_stgt_with_foundation_sample(foundation_sample) -> None:
    model = PFSTGT()
    model.eval()

    node = torch.from_numpy(foundation_sample.x_temporal.node_features).float().unsqueeze(0)
    global_ = torch.from_numpy(foundation_sample.x_temporal.global_features).float().unsqueeze(0)
    adj = torch.from_numpy(foundation_sample.x_graph.adjacency).float()
    bias = torch.from_numpy(foundation_sample.x_graph.attention_bias).float()

    with torch.no_grad():
        output = model(
            node,
            global_,
            adj,
            attention_bias=bias,
            return_attention=True,
        )

    assert output.demand_pred.shape == (1, N_NODES)
    assert output.osi_pred.shape == (1, 1)
    assert np.isfinite(output.demand_pred.numpy()).all()
    assert np.isfinite(output.osi_pred.numpy()).all()
    assert output.attn_spatial is not None
    assert output.attn_temporal is not None
