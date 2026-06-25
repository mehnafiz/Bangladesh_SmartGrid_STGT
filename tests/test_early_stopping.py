"""Tests for early stopping."""

from __future__ import annotations

from training.early_stopping import EarlyStopping


def test_early_stopping_improves() -> None:
    es = EarlyStopping(patience=2, min_delta=0.01)
    s1 = es.step(10.0)
    assert s1.improved
    assert not s1.should_stop


def test_early_stopping_triggers() -> None:
    es = EarlyStopping(patience=2, min_delta=0.01)
    es.step(10.0)
    es.step(10.5)
    es.step(10.4)
    s = es.step(10.3)
    assert s.should_stop
