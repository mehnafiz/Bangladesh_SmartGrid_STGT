"""P3 graph pipeline orchestrator."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from graph.bias import AdjacencyBias
from graph.registry import GraphRegistry, GraphVariant
from graph.types import XGraph
from utils.logging import get_logger

logger = get_logger(__name__)


@dataclass(frozen=True)
class GraphPipelineResult:
    x_graph: XGraph


class GraphPipeline:
    """Load adjacency and construct graph tensors."""

    def __init__(
        self,
        variant: GraphVariant = GraphVariant.HYBRID,
        train_clean: pd.DataFrame | None = None,
    ) -> None:
        self.variant = variant
        self.registry = GraphRegistry(train_clean=train_clean)
        self.bias_builder = AdjacencyBias()

    def build(self) -> GraphPipelineResult:
        adjacency = self.registry.get(self.variant)
        bias = self.bias_builder.build(adjacency)
        x_graph = XGraph(
            adjacency=adjacency,
            attention_bias=bias,
            variant=self.variant.value,
        )
        logger.debug(
            "Built X_graph variant=%s edges=%s",
            x_graph.variant,
            int((adjacency > 0).sum() // 2),
        )
        return GraphPipelineResult(x_graph=x_graph)
