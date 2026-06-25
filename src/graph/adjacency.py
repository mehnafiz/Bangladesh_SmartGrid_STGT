"""Hybrid adjacency matrix loading."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from constants import DEFAULT_ADJACENCY_PATH, N_NODES, PROJECT_ROOT, REGIONS
from utils.exceptions import GraphValidationError
from utils.logging import get_logger

logger = get_logger(__name__)


def load_adjacency_matrix(path: Path | None = None) -> np.ndarray:
    """Load row-normalised adjacency matrix aligned to REGIONS order."""
    loader = AdjacencyLoader(path)
    return loader.load()


class AdjacencyLoader:
    """Load and validate the Phase 08 hybrid adjacency CSV."""

    def __init__(self, path: Path | None = None) -> None:
        self.path = path or (PROJECT_ROOT / DEFAULT_ADJACENCY_PATH.relative_to(PROJECT_ROOT))

    def load(self) -> np.ndarray:
        if not self.path.exists():
            raise FileNotFoundError(f"Adjacency matrix not found: {self.path}")

        df = pd.read_csv(self.path, index_col=0)
        missing = [r for r in REGIONS if r not in df.index or r not in df.columns]
        if missing:
            raise GraphValidationError(f"Adjacency missing regions: {missing}")

        matrix = df.loc[list(REGIONS), list(REGIONS)].astype(np.float32).to_numpy()
        self._validate(matrix)
        logger.info("Loaded adjacency matrix from %s", self.path.name)
        return matrix

    @staticmethod
    def _validate(matrix: np.ndarray) -> None:
        if matrix.shape != (N_NODES, N_NODES):
            raise GraphValidationError(f"Expected shape ({N_NODES},{N_NODES}), got {matrix.shape}")
        if np.any(matrix < 0):
            raise GraphValidationError("Adjacency contains negative weights")
        if not np.allclose(np.diag(matrix), 0.0):
            raise GraphValidationError("Adjacency diagonal must be zero")
        if (matrix > 0).sum() // 2 != 24:
            logger.warning(
                "Hybrid edge count is %s undirected edges (expected 24)",
                (matrix > 0).sum() // 2,
            )

    @staticmethod
    def row_normalize(matrix: np.ndarray) -> np.ndarray:
        """Row-normalise non-negative adjacency for message passing."""
        out = matrix.copy().astype(np.float32)
        for i in range(out.shape[0]):
            row_sum = out[i].sum()
            if row_sum > 0:
                out[i] /= row_sum
        return out
