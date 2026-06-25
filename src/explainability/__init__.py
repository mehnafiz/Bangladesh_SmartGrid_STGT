"""PF-STGT explainability framework."""

from explainability.attention_extractor import AttentionExtractor
from explainability.coalitions import COALITION_REGISTRY, coalition_ids_for_task
from explainability.config import ExplainabilityConfig
from explainability.node_attribution import NodeAttributor
from explainability.permutation import PermutationImportance
from explainability.shap_engine import ShapEngine
from explainability.stress_attribution import StressAttributor
from explainability.temporal_attribution import TemporalAttributor
from explainability.types import (
    GroupedShapValues,
    NodeAttributionResult,
    OSIComponentDecomposition,
    PermutationImportanceResult,
    ShapExplanationResult,
    SpatialAttentionResult,
    StressAttributionResult,
    TemporalAttributionResult,
    TemporalAttentionResult,
)

__all__ = [
    "AttentionExtractor",
    "COALITION_REGISTRY",
    "ExplainabilityConfig",
    "GroupedShapValues",
    "NodeAttributionResult",
    "NodeAttributor",
    "OSIComponentDecomposition",
    "PermutationImportance",
    "PermutationImportanceResult",
    "ShapEngine",
    "ShapExplanationResult",
    "SpatialAttentionResult",
    "StressAttributionResult",
    "StressAttributor",
    "TemporalAttentionResult",
    "TemporalAttributionResult",
    "TemporalAttributor",
    "coalition_ids_for_task",
]
