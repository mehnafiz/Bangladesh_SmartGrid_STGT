"""Typed result containers for explainability outputs."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass(frozen=True)
class SpatialAttentionResult:
    """Aggregated spatial attention for one or more samples."""

    influence_matrix: np.ndarray
    per_head: np.ndarray | None = None


@dataclass(frozen=True)
class TemporalAttentionResult:
    """Aggregated temporal attention weights α_t over lookback window."""

    alpha_t: np.ndarray
    per_head: np.ndarray | None = None


@dataclass(frozen=True)
class GroupedShapValues:
    """Coalition-level SHAP attributions."""

    group_ids: tuple[str, ...]
    phi: np.ndarray
    task: str
    region_index: int | None = None


@dataclass(frozen=True)
class ShapExplanationResult:
    """Local or global SHAP explanation bundle."""

    grouped: GroupedShapValues
    node_attributions: np.ndarray | None = None
    global_attributions: np.ndarray | None = None


@dataclass(frozen=True)
class PermutationImportanceEntry:
    group_id: str
    mean_delta: float
    std_delta: float


@dataclass(frozen=True)
class PermutationImportanceResult:
    task: str
    entries: tuple[PermutationImportanceEntry, ...]
    baseline_score: float


@dataclass(frozen=True)
class NodeImportanceRow:
    node: str
    shap_mass: float
    attention_inflow: float
    attention_outflow: float
    demand_share: float | None = None
    contribution: float | None = None


@dataclass(frozen=True)
class NodeAttributionResult:
    rows: tuple[NodeImportanceRow, ...]
    dhaka_index: int


@dataclass(frozen=True)
class TemporalAttributionResult:
    alpha_t: np.ndarray
    top_k_indices: tuple[int, ...]
    top_k_weights: tuple[float, ...]


@dataclass(frozen=True)
class OSIComponentDecomposition:
    c1_raw: float
    c2_raw: float
    c3_raw: float
    c1_norm: float
    c2_norm: float
    c3_norm: float
    driver: str


@dataclass(frozen=True)
class StressAttributionResult:
    grouped_shap: GroupedShapValues
    components: OSIComponentDecomposition
    top_shap_group: str
    driver_agreement: bool
    notes: tuple[str, ...] = field(default_factory=tuple)
