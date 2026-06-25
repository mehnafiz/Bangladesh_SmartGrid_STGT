"""Target batch datatypes."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from constants import N_NODES


@dataclass(frozen=True)
class YDemand:
    """Regional demand targets in raw MW."""

    values: np.ndarray

    def __post_init__(self) -> None:
        if self.values.shape != (N_NODES,):
            raise ValueError(f"y_demand shape must be ({N_NODES},)")


@dataclass(frozen=True)
class YOSI:
    """Operational stress index target in [0, 1]."""

    value: float

    def __post_init__(self) -> None:
        if not 0.0 <= self.value <= 1.0:
            raise ValueError(f"y_osi must be in [0, 1], got {self.value}")


@dataclass(frozen=True)
class TargetBatch:
    """Combined Sprint 01 target outputs."""

    y_demand: YDemand
    y_osi: YOSI
    target_idx: int
    include_stress: bool = True

    @property
    def demand_array(self) -> np.ndarray:
        return self.y_demand.values

    @property
    def osi_scalar(self) -> float:
        return self.y_osi.value
