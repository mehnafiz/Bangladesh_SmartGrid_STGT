"""Tests for feature coalition registry."""

from __future__ import annotations

import torch

from explainability.coalitions import (
    GLOBAL_FEATURES,
    NODE_FEATURES_PER_REGION,
    coalition_ids_for_task,
    global_coalition_mask,
    node_coalition_mask,
)


def test_demand_coalition_count() -> None:
    groups = coalition_ids_for_task("demand")
    assert len(groups) == 10
    assert "G11" not in groups


def test_stress_coalition_includes_g11() -> None:
    groups = coalition_ids_for_task("stress")
    assert "G11" in groups
    assert "G2" not in groups


def test_node_coalition_mask_shape() -> None:
    mask = node_coalition_mask("G4")
    assert mask.shape == (NODE_FEATURES_PER_REGION,)
    assert mask.sum().item() == 4


def test_global_coalition_mask_shape() -> None:
    mask = global_coalition_mask("G8")
    assert mask.shape == (GLOBAL_FEATURES,)
    assert mask.sum().item() == 5
