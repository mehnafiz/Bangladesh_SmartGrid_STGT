"""P2 — Feature pipeline: temporal tensor construction."""

from features.global_features import GlobalFeatureBuilder
from features.leakage_guard import LeakageGuard, assert_no_osi_in_inputs
from features.node_features import NodeFeatureBuilder
from features.specs import (
    EXCLUDED_INPUT_FEATURES,
    GLOBAL_INPUT_FEATURE_NAMES,
    NODE_INPUT_FEATURE_TEMPLATES,
    global_feature_columns,
    node_feature_columns,
)
from features.temporal import TemporalBatch, XTemporal
from features.window_builder import WindowBuilder

__all__ = [
    "EXCLUDED_INPUT_FEATURES",
    "GLOBAL_INPUT_FEATURE_NAMES",
    "GlobalFeatureBuilder",
    "LeakageGuard",
    "NODE_INPUT_FEATURE_TEMPLATES",
    "NodeFeatureBuilder",
    "TemporalBatch",
    "WindowBuilder",
    "XTemporal",
    "assert_no_osi_in_inputs",
    "global_feature_columns",
    "node_feature_columns",
]

def __getattr__(name: str):
    if name == "FeaturePipeline":
        from features.pipeline import FeaturePipeline

        return FeaturePipeline
    raise AttributeError(name)
