"""End-to-end Sprint 01 foundation tests."""

from __future__ import annotations

from constants import GLOBAL_FEATURES, INPUT_WINDOW_T, N_NODES, NODE_FEATURES_PER_REGION
from foundation import FoundationCoordinator


def test_foundation_coordinator_smoke() -> None:
    coordinator = FoundationCoordinator(verify_md5=True)
    sample = coordinator.smoke_sample("train")

    assert sample.x_temporal.node_features.shape == (
        INPUT_WINDOW_T,
        N_NODES,
        NODE_FEATURES_PER_REGION,
    )
    assert sample.x_temporal.global_features.shape == (INPUT_WINDOW_T, GLOBAL_FEATURES)
    assert sample.x_graph.adjacency.shape == (N_NODES, N_NODES)
    assert sample.targets.y_demand.values.shape == (N_NODES,)
    assert 0.0 <= sample.targets.y_osi.value <= 1.0


def test_all_splits_produce_samples() -> None:
    coordinator = FoundationCoordinator(verify_md5=True)
    for split in ("train", "validation", "test"):
        sample = coordinator.smoke_sample(split)
        assert sample.split == split
