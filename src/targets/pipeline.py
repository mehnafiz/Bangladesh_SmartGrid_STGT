"""P4 target pipeline orchestrator."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from data.splits import SampleIndex
from targets.batch import TargetBatch
from targets.demand import DemandTargetBuilder
from targets.osi import OSITargetBuilder
from utils.logging import get_logger

logger = get_logger(__name__)


@dataclass(frozen=True)
class TargetPipelineResult:
    batch: TargetBatch


class TargetPipeline:
    """Generate demand and OSI targets for a sample index."""

    def __init__(self, train_clean: pd.DataFrame) -> None:
        self.demand_builder = DemandTargetBuilder()
        self.osi_builder = OSITargetBuilder(train_clean)

    def build(
        self,
        clean: pd.DataFrame,
        sample: SampleIndex,
        *,
        include_stress: bool = True,
    ) -> TargetPipelineResult:
        y_demand = self.demand_builder.build(clean, sample.target_idx)
        y_osi = self.osi_builder.build(clean, sample.target_idx)
        batch = TargetBatch(
            y_demand=y_demand,
            y_osi=y_osi,
            target_idx=sample.target_idx,
            include_stress=include_stress,
        )
        logger.debug(
            "Built targets target_idx=%s demand_mean=%.2f osi=%.4f",
            sample.target_idx,
            float(y_demand.values.mean()),
            y_osi.value,
        )
        return TargetPipelineResult(batch=batch)
