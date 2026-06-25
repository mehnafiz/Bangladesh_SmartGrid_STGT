"""Tests for P4 target pipeline."""

from __future__ import annotations

import numpy as np
import pytest

from constants import N_NODES
from data.loader import DataStore
from data.splits import SplitManager
from targets.pipeline import TargetPipeline


@pytest.fixture(scope="module")
def target_pipeline() -> TargetPipeline:
    store = DataStore(verify_md5=True)
    return TargetPipeline(store.get_split("train").clean)


def test_y_demand_shape_and_positive(target_pipeline: TargetPipeline) -> None:
    store = DataStore(verify_md5=True)
    split = store.get_split("train")
    sample = SplitManager().sample_indices(split.features)[100]
    result = target_pipeline.build(split.clean, sample)
    assert result.batch.y_demand.values.shape == (N_NODES,)
    assert (result.batch.y_demand.values > 0).all()


def test_y_osi_bounded(target_pipeline: TargetPipeline) -> None:
    store = DataStore(verify_md5=True)
    split = store.get_split("train")
    sample = SplitManager().sample_indices(split.features)[100]
    result = target_pipeline.build(split.clean, sample)
    assert 0.0 <= result.batch.y_osi.value <= 1.0


def test_demand_uses_raw_mw_not_scaled(target_pipeline: TargetPipeline) -> None:
    store = DataStore(verify_md5=True)
    split = store.get_split("train")
    sample = SplitManager().sample_indices(split.features)[100]
    result = target_pipeline.build(split.clean, sample)
    assert (result.batch.y_demand.values > 100.0).all()
