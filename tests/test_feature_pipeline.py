"""Tests for P2 feature pipeline."""

from __future__ import annotations

import numpy as np
import pytest

from constants import GLOBAL_FEATURES, INPUT_WINDOW_T, N_NODES, NODE_FEATURES_PER_REGION
from data.loader import DataStore
from features.leakage_guard import LeakageGuard
from features.pipeline import FeaturePipeline
from features.specs import GLOBAL_INPUT_FEATURE_NAMES


@pytest.fixture(scope="module")
def feature_pipeline() -> FeaturePipeline:
    return FeaturePipeline()


@pytest.fixture(scope="module")
def train_features() -> "pd.DataFrame":
    from data.loader import DataStore

    store = DataStore(verify_md5=True)
    return store.get_split("train").features


def test_leakage_guard_excludes_osi() -> None:
    LeakageGuard.validate_global_names()
    assert "operational_stress_index" not in GLOBAL_INPUT_FEATURE_NAMES


def test_x_temporal_shapes(
    feature_pipeline: FeaturePipeline,
    train_features,
) -> None:
    end_idx = 20
    result = feature_pipeline.build_sample(train_features, end_idx)
    assert result.x_temporal.node_features.shape == (
        INPUT_WINDOW_T,
        N_NODES,
        NODE_FEATURES_PER_REGION,
    )
    assert result.x_temporal.global_features.shape == (INPUT_WINDOW_T, GLOBAL_FEATURES)
    assert np.isfinite(result.x_temporal.node_features).all()
    assert np.isfinite(result.x_temporal.global_features).all()


def test_window_rejects_early_index(
    feature_pipeline: FeaturePipeline,
    train_features,
) -> None:
    with pytest.raises(Exception):
        feature_pipeline.build_sample(train_features, 5)
