"""Permutation importance for coalition validation (Phase 12)."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import numpy as np
import torch
from torch import Tensor, nn
from torch.utils.data import DataLoader

from explainability.coalitions import (
    GLOBAL_FEATURE_GROUPS,
    NODE_FEATURE_GROUPS,
    coalition_ids_for_task,
    global_coalition_mask,
)
from explainability.config import ExplainabilityConfig
from explainability.types import PermutationImportanceEntry, PermutationImportanceResult
from utils.logging import get_logger

logger = get_logger(__name__)

TaskName = Literal["demand", "stress"]


class PermutationImportance:
    """
    Coalition-level permutation importance on validation data.

    Shuffles coalition features across the batch and measures metric degradation.
    """

    def __init__(
        self,
        model: nn.Module,
        config: ExplainabilityConfig | None = None,
    ) -> None:
        self.model = model
        self.config = config or ExplainabilityConfig()
        self.device = torch.device(self.config.device)
        self.model.to(self.device)
        self.model.eval()

    def compute(
        self,
        dataloader: DataLoader,
        *,
        task: TaskName,
        max_batches: int | None = None,
        n_repeats: int | None = None,
    ) -> PermutationImportanceResult:
        repeats = n_repeats or self.config.permutation_repeats
        batches = self._collect_batches(dataloader, max_batches)
        if not batches:
            raise ValueError("Permutation importance requires at least one batch")

        baseline = self._score_batches(batches, task=task)
        entries: list[PermutationImportanceEntry] = []

        for group_id in coalition_ids_for_task(task):
            deltas: list[float] = []
            for _ in range(repeats):
                permuted = [self._permute_batch(batch, group_id) for batch in batches]
                score = self._score_batches(permuted, task=task)
                deltas.append(max(0.0, score - baseline))
            entries.append(
                PermutationImportanceEntry(
                    group_id=group_id,
                    mean_delta=float(np.mean(deltas)),
                    std_delta=float(np.std(deltas)),
                )
            )
            logger.debug(
                "Permutation group=%s mean_delta=%.6f",
                group_id,
                entries[-1].mean_delta,
            )

        ranked = sorted(entries, key=lambda item: item.mean_delta, reverse=True)
        return PermutationImportanceResult(
            task=task,
            entries=tuple(ranked),
            baseline_score=baseline,
        )

    def spearman_vs_shap(
        self,
        permutation: PermutationImportanceResult,
        grouped_shap: np.ndarray,
        group_ids: tuple[str, ...],
    ) -> float:
        """Spearman ρ between permutation ranks and |SHAP φ| ranks."""
        from scipy.stats import spearmanr

        perm_map = {entry.group_id: entry.mean_delta for entry in permutation.entries}
        perm_vals = [perm_map[gid] for gid in group_ids]
        shap_vals = np.abs(grouped_shap)
        if len(perm_vals) < 2:
            return 0.0
        rho, _ = spearmanr(perm_vals, shap_vals)
        if np.isnan(rho):
            return 0.0
        return float(rho)

    def save_csv(self, result: PermutationImportanceResult, path: Path) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        lines = ["group_id,mean_delta,std_delta,task,baseline_score"]
        for entry in result.entries:
            lines.append(
                f"{entry.group_id},{entry.mean_delta:.8f},{entry.std_delta:.8f},"
                f"{result.task},{result.baseline_score:.8f}"
            )
        path.write_text("\n".join(lines))
        logger.info("Saved permutation importance CSV -> %s", path)
        return path

    def _collect_batches(
        self,
        dataloader: DataLoader,
        max_batches: int | None,
    ) -> list[dict[str, Tensor]]:
        batches: list[dict[str, Tensor]] = []
        for batch_idx, batch in enumerate(dataloader):
            if max_batches is not None and batch_idx >= max_batches:
                break
            batches.append(batch)
        return batches

    def _score_batches(self, batches: list[dict[str, Tensor]], *, task: TaskName) -> float:
        demand_errors: list[float] = []
        stress_errors: list[float] = []

        with torch.no_grad():
            for batch in batches:
                batch = self._to_device(batch)
                output = self.model(
                    batch["node_features"],
                    batch["global_features"],
                    batch["adjacency"],
                    attention_bias=batch.get("attention_bias"),
                )
                if task == "demand":
                    err = torch.mean(
                        torch.abs(output.demand_pred - batch["demand_target"])
                    ).item()
                    demand_errors.append(err)
                else:
                    err = torch.mean(
                        (output.osi_pred - batch["osi_target"]) ** 2
                    ).item()
                    stress_errors.append(err)

        if task == "demand":
            return float(np.mean(demand_errors))
        return float(np.mean(stress_errors))

    def _permute_batch(self, batch: dict[str, Tensor], group_id: str) -> dict[str, Tensor]:
        permuted = {key: value.clone() if torch.is_tensor(value) else value for key, value in batch.items()}
        node = permuted["node_features"]
        global_ = permuted["global_features"]

        if group_id in NODE_FEATURE_GROUPS:
            feat_indices = NODE_FEATURE_GROUPS[group_id]
            for feat_idx in feat_indices:
                column = node[:, :, :, feat_idx].clone()
                perm = torch.randperm(column.shape[0], device=column.device)
                node[:, :, :, feat_idx] = column[perm]
        elif group_id in GLOBAL_FEATURE_GROUPS:
            feat_indices = GLOBAL_FEATURE_GROUPS[group_id]
            for feat_idx in feat_indices:
                column = global_[:, :, feat_idx].clone()
                perm = torch.randperm(column.shape[0], device=column.device)
                global_[:, :, feat_idx] = column[perm]

        return permuted

    def _to_device(self, batch: dict[str, Tensor]) -> dict[str, Tensor]:
        return {
            key: value.to(self.device) if torch.is_tensor(value) else value
            for key, value in batch.items()
        }
