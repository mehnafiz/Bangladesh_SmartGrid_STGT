"""Early stopping on validation metric (Phase 10)."""

from __future__ import annotations

from dataclasses import dataclass

from utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class EarlyStoppingState:
    best_score: float
    epochs_without_improvement: int
    should_stop: bool
    improved: bool


class EarlyStopping:
    """
    Monitor validation macro demand MAE (lower is better).

    Phase 10: patience=15, min_delta=0.01 MW.
    """

    def __init__(
        self,
        patience: int = 15,
        min_delta: float = 0.01,
    ) -> None:
        self.patience = patience
        self.min_delta = min_delta
        self.best_score: float | None = None
        self.epochs_without_improvement = 0

    def step(self, score: float) -> EarlyStoppingState:
        improved = False
        if self.best_score is None or score < self.best_score - self.min_delta:
            self.best_score = score
            self.epochs_without_improvement = 0
            improved = True
            logger.debug("EarlyStopping improvement: score=%.4f", score)
        else:
            self.epochs_without_improvement += 1
            logger.debug(
                "EarlyStopping no improvement: %s/%s (score=%.4f best=%.4f)",
                self.epochs_without_improvement,
                self.patience,
                score,
                self.best_score if self.best_score is not None else score,
            )

        should_stop = self.epochs_without_improvement >= self.patience
        if should_stop:
            logger.info("Early stopping triggered at score=%.4f", score)

        return EarlyStoppingState(
            best_score=self.best_score if self.best_score is not None else score,
            epochs_without_improvement=self.epochs_without_improvement,
            should_stop=should_stop,
            improved=improved,
        )

    def reset(self) -> None:
        self.best_score = None
        self.epochs_without_improvement = 0
