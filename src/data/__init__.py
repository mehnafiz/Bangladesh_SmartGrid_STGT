"""P1 — Data pipeline: load, validate, and expose split datasets."""

from data.loader import DataStore, SplitFrames
from data.splits import SampleIndex, SplitManager
from data.validators import DataValidator, ValidationIssue, ValidationReport

__all__ = [
    "DataStore",
    "DataValidator",
    "SplitFrames",
    "SplitManager",
    "SampleIndex",
    "ValidationIssue",
    "ValidationReport",
]


def __getattr__(name: str):
    if name == "DataPipeline":
        from data.pipeline import DataPipeline

        return DataPipeline
    raise AttributeError(name)
