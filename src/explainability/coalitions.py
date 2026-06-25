"""Feature coalition registry for grouped SHAP and permutation (Phase 12)."""

from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import Tensor

from constants import GLOBAL_FEATURES, N_NODES, NODE_FEATURES_PER_REGION, REGIONS

NODE_FEATURE_GROUPS: dict[str, tuple[int, ...]] = {
    "G1": (0,),
    "G2": (1,),
    "G3": (2,),
    "G4": (3, 4, 5, 6),
    "G5": (7, 8),
}

GLOBAL_FEATURE_GROUPS: dict[str, tuple[int, ...]] = {
    "G6": (0, 1, 2, 3, 16),
    "G7": (4, 5, 6),
    "G8": (8, 10, 11, 12, 13),
    "G9": (7,),
    "G10": (14, 15),
    "G11": (9,),
}

TASK_COALITIONS: dict[str, tuple[str, ...]] = {
    "demand": ("G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10"),
    "stress": ("G1", "G3", "G5", "G6", "G7", "G8", "G10", "G11"),
}

NODE_LOCAL_GROUPS: tuple[str, ...] = ("G1", "G2", "G3", "G4", "G5")


@dataclass(frozen=True)
class CoalitionSpec:
    group_id: str
    group_name: str
    scope: str
    tasks: tuple[str, ...]


COALITION_REGISTRY: tuple[CoalitionSpec, ...] = (
    CoalitionSpec("G1", "regional_demand_block", "node", ("demand", "stress")),
    CoalitionSpec("G2", "regional_supply_block", "node", ("demand",)),
    CoalitionSpec("G3", "regional_load_block", "node", ("demand", "stress")),
    CoalitionSpec("G4", "engineered_lags_rolling", "node", ("demand",)),
    CoalitionSpec("G5", "regional_share_intensity", "node", ("demand", "stress")),
    CoalitionSpec("G6", "calendar_trend", "global", ("demand", "stress")),
    CoalitionSpec("G7", "grid_aggregates", "global", ("demand", "stress")),
    CoalitionSpec("G8", "limitation_stack", "global", ("demand", "stress")),
    CoalitionSpec("G9", "weather_anomaly", "global", ("demand",)),
    CoalitionSpec("G10", "national_generation_scalars", "global", ("demand", "stress")),
    CoalitionSpec("G11", "shedding_indicator", "global", ("stress",)),
)


def coalition_ids_for_task(task: str) -> tuple[str, ...]:
    if task not in TASK_COALITIONS:
        raise ValueError(f"Unknown task: {task}")
    return TASK_COALITIONS[task]


def node_coalition_mask(
    group_id: str,
    *,
    node_index: int | None = None,
    device: torch.device | None = None,
) -> Tensor:
    """Boolean mask over node feature tensor (T, N, F_n)."""
    if group_id not in NODE_FEATURE_GROUPS:
        raise ValueError(f"Unknown node coalition: {group_id}")

    mask = torch.zeros(NODE_FEATURES_PER_REGION, dtype=torch.bool, device=device)
    for feat_idx in NODE_FEATURE_GROUPS[group_id]:
        mask[feat_idx] = True

    if node_index is None:
        return mask
    if node_index < 0 or node_index >= N_NODES:
        raise ValueError(f"node_index out of range: {node_index}")
    return mask


def global_coalition_mask(group_id: str, *, device: torch.device | None = None) -> Tensor:
    """Boolean mask over global feature vector (F_g,)."""
    if group_id not in GLOBAL_FEATURE_GROUPS:
        raise ValueError(f"Unknown global coalition: {group_id}")

    mask = torch.zeros(GLOBAL_FEATURES, dtype=torch.bool, device=device)
    for feat_idx in GLOBAL_FEATURE_GROUPS[group_id]:
        mask[feat_idx] = True
    return mask


def node_shap_groups() -> tuple[str, ...]:
    return NODE_LOCAL_GROUPS


def region_name(index: int) -> str:
    return REGIONS[index]
