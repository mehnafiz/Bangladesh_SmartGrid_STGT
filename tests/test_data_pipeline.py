"""Tests for P1 data pipeline."""

from __future__ import annotations

import pytest

from constants import SPLIT_SPECS
from data.loader import DataStore
from data.pipeline import DataPipeline
from data.splits import SplitManager


@pytest.fixture(scope="module")
def data_store() -> DataStore:
    return DataStore(verify_md5=True)


def test_locked_md5_verification(data_store: DataStore) -> None:
    assert len(data_store.all_splits()) == 3


def test_split_row_counts(data_store: DataStore) -> None:
    for name, split in data_store.all_splits().items():
        assert len(split.features) == SPLIT_SPECS[name].expected_rows
        assert len(split.clean) == len(split.features)


def test_data_pipeline_validation() -> None:
    result = DataPipeline(verify_md5=True, validate=True).run()
    assert all(report.passed for report in result.validation_reports.values())
    assert len(result.sample_indices["train"]) > 0


def test_split_boundaries_non_overlapping(data_store: DataStore) -> None:
    frames = {name: s.features for name, s in data_store.all_splits().items()}
    SplitManager().validate_boundaries(frames)


def test_sample_index_targets_are_next_day(data_store: DataStore) -> None:
    split = data_store.get_split("train")
    manager = SplitManager()
    sample = manager.sample_indices(split.features)[0]
    assert sample.target_idx == sample.end_idx + 1
    assert sample.date_target > sample.date_end


def test_split_manager_rejects_underflow() -> None:
    manager = SplitManager()
    with pytest.raises(ValueError):
        manager.window_slice(2)
