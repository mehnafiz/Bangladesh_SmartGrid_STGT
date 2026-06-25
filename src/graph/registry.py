"""Graph variant registry for hybrid / geo / correlation ablations."""

from __future__ import annotations

from enum import Enum
from pathlib import Path

import numpy as np
import pandas as pd

from constants import (
    CORRELATION_THRESHOLD,
    DEFAULT_ADJACENCY_PATH,
    GEOGRAPHIC_NEIGHBORS,
    PROJECT_ROOT,
    REGIONS,
    STRONG_CORRELATION_THRESHOLD,
)
from graph.adjacency import AdjacencyLoader
from utils.logging import get_logger

logger = get_logger(__name__)


class GraphVariant(str, Enum):
    HYBRID = "hybrid"
    GEO = "geo"
    CORR = "corr"


class GraphRegistry:
    """Provide adjacency matrices for default and ablation graph variants."""

    def __init__(
        self,
        root: Path | None = None,
        train_clean: pd.DataFrame | None = None,
    ) -> None:
        self.root = root or PROJECT_ROOT
        self.train_clean = train_clean
        self._cache: dict[str, np.ndarray] = {}

    def get(self, variant: GraphVariant | str = GraphVariant.HYBRID) -> np.ndarray:
        key = GraphVariant(variant).value if not isinstance(variant, GraphVariant) else variant.value
        if key not in self._cache:
            self._cache[key] = self._build(GraphVariant(key))
        return self._cache[key]

    def _build(self, variant: GraphVariant) -> np.ndarray:
        if variant is GraphVariant.HYBRID:
            path = self.root / DEFAULT_ADJACENCY_PATH.relative_to(PROJECT_ROOT)
            return AdjacencyLoader(path).load()

        corr = self._demand_correlation_matrix()
        if variant is GraphVariant.GEO:
            return self._geographic_graph()
        if variant is GraphVariant.CORR:
            return self._correlation_graph(corr)
        raise ValueError(f"Unsupported graph variant: {variant}")

    def _demand_correlation_matrix(self) -> np.ndarray:
        if self.train_clean is None:
            raise ValueError("train_clean dataframe required for geo/corr graph variants")
        cols = [f"{r}_demand" for r in REGIONS]
        corr = self.train_clean[cols].corr().astype(np.float32).to_numpy()
        return corr

    @staticmethod
    def _geographic_graph() -> np.ndarray:
        idx = {name: i for i, name in enumerate(REGIONS)}
        matrix = np.zeros((len(REGIONS), len(REGIONS)), dtype=np.float32)
        for region, neighbors in GEOGRAPHIC_NEIGHBORS.items():
            i = idx[region]
            for neighbor in neighbors:
                matrix[i, idx[neighbor]] = 1.0
        matrix = np.maximum(matrix, matrix.T)
        np.fill_diagonal(matrix, 0.0)
        return AdjacencyLoader.row_normalize(matrix)

    @staticmethod
    def _correlation_graph(corr: np.ndarray) -> np.ndarray:
        weighted = corr.copy()
        np.fill_diagonal(weighted, 0.0)
        mask = weighted >= CORRELATION_THRESHOLD
        weighted = weighted * mask
        logger.debug(
            "Built correlation graph with threshold %.2f", CORRELATION_THRESHOLD
        )
        return AdjacencyLoader.row_normalize(weighted)

    @staticmethod
    def build_hybrid_from_correlation(corr: np.ndarray) -> np.ndarray:
        """Construct hybrid graph using Phase 08 rule (for validation/tests)."""
        geo = GraphRegistry._geographic_graph() > 0
        weighted = corr.copy().astype(np.float32)
        np.fill_diagonal(weighted, 0.0)
        hybrid_mask = geo | (weighted >= STRONG_CORRELATION_THRESHOLD)
        hybrid = weighted * hybrid_mask
        return AdjacencyLoader.row_normalize(hybrid)
