"""GradientSHAP-style grouped feature attribution (Phase 12 L1)."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import numpy as np
import torch
from torch import Tensor, nn

from explainability.coalitions import (
    GLOBAL_FEATURE_GROUPS,
    NODE_FEATURE_GROUPS,
    coalition_ids_for_task,
    global_coalition_mask,
    node_coalition_mask,
)
from explainability.config import ExplainabilityConfig
from explainability.types import GroupedShapValues, ShapExplanationResult
from utils.logging import get_logger

logger = get_logger(__name__)

TaskName = Literal["demand", "stress"]


class ShapEngine:
    """
    Grouped GradientSHAP attributions for PF-STGT.

    Uses a Captum-compatible integrated-gradients loop (GradientSHAP approximation)
    over coalition-masked node/global inputs.
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

    def explain_local(
        self,
        batch: dict[str, Tensor],
        *,
        task: TaskName,
        region_index: int | None = None,
        baseline: dict[str, Tensor] | None = None,
    ) -> ShapExplanationResult:
        """Compute coalition-level attributions for a single sample."""
        sample = self._select_batch_index(batch, 0)
        base = baseline or self._zero_baseline(sample)
        node_attr, global_attr = self._integrated_gradients(
            sample,
            baseline=base,
            task=task,
            region_index=region_index,
        )
        grouped = self._aggregate_coalitions(
            node_attr,
            global_attr,
            task=task,
            region_index=region_index,
        )
        return ShapExplanationResult(
            grouped=grouped,
            node_attributions=node_attr.detach().cpu().numpy(),
            global_attributions=global_attr.detach().cpu().numpy(),
        )

    def explain_global(
        self,
        batches: list[dict[str, Tensor]],
        *,
        task: TaskName,
        region_index: int | None = None,
        max_samples: int | None = None,
    ) -> ShapExplanationResult:
        """Average absolute coalition attributions over multiple samples."""
        limit = max_samples or len(batches)
        phi_sum: dict[str, float] = {gid: 0.0 for gid in coalition_ids_for_task(task)}
        count = 0
        last_node_attr: Tensor | None = None
        last_global_attr: Tensor | None = None

        for batch in batches[:limit]:
            local = self.explain_local(batch, task=task, region_index=region_index)
            for gid, value in zip(local.grouped.group_ids, local.grouped.phi, strict=True):
                phi_sum[gid] += abs(float(value))
            last_node_attr = torch.as_tensor(local.node_attributions)
            last_global_attr = torch.as_tensor(local.global_attributions)
            count += 1

        if count == 0:
            raise ValueError("No batches provided for global SHAP")

        group_ids = coalition_ids_for_task(task)
        phi = np.array([phi_sum[gid] / count for gid in group_ids], dtype=np.float64)
        grouped = GroupedShapValues(
            group_ids=group_ids,
            phi=phi,
            task=task,
            region_index=region_index,
        )
        logger.info(
            "Global grouped SHAP computed over %s samples for task=%s",
            count,
            task,
        )
        return ShapExplanationResult(
            grouped=grouped,
            node_attributions=last_node_attr.numpy() if last_node_attr is not None else None,
            global_attributions=last_global_attr.numpy() if last_global_attr is not None else None,
        )

    def rank_groups(self, grouped: GroupedShapValues) -> list[tuple[str, float]]:
        """Return coalition IDs sorted by descending |φ|."""
        pairs = list(zip(grouped.group_ids, grouped.phi, strict=True))
        return sorted(pairs, key=lambda item: abs(item[1]), reverse=True)

    def save_grouped_csv(
        self,
        grouped: GroupedShapValues,
        path: Path,
        *,
        date_label: str | None = None,
    ) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        lines = ["group_id,phi,task,region_index,date"]
        region = "" if grouped.region_index is None else str(grouped.region_index)
        label = date_label or ""
        for gid, phi in zip(grouped.group_ids, grouped.phi, strict=True):
            lines.append(f"{gid},{phi:.8f},{grouped.task},{region},{label}")
        path.write_text("\n".join(lines))
        logger.info("Saved grouped SHAP CSV -> %s", path)
        return path

    def save_summary_plot(
        self,
        grouped: GroupedShapValues,
        path: Path,
    ) -> Path | None:
        """Save a grouped bar chart (beeswarm substitute for coalition SHAP)."""
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            logger.warning("matplotlib unavailable; skipping SHAP summary plot")
            return None

        path.parent.mkdir(parents=True, exist_ok=True)
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(list(grouped.group_ids), grouped.phi)
        ax.set_title(f"Grouped SHAP — {grouped.task}")
        ax.set_ylabel("φ")
        fig.tight_layout()
        fig.savefig(path, dpi=150)
        plt.close(fig)
        logger.info("Saved SHAP summary plot -> %s", path)
        return path

    def _integrated_gradients(
        self,
        sample: dict[str, Tensor],
        *,
        baseline: dict[str, Tensor],
        task: TaskName,
        region_index: int | None,
    ) -> tuple[Tensor, Tensor]:
        node = sample["node_features"].detach()
        global_ = sample["global_features"].detach()
        adjacency = sample["adjacency"].detach()
        bias = sample.get("attention_bias")
        if bias is not None:
            bias = bias.detach()

        def forward(node_in: Tensor, global_in: Tensor) -> Tensor:
            output = self.model(
                node_in.unsqueeze(0),
                global_in.unsqueeze(0),
                adjacency,
                attention_bias=bias,
            )
            if task == "demand":
                idx = region_index if region_index is not None else 0
                return output.demand_pred[:, idx]
            return output.osi_pred.squeeze(-1)

        node_base = baseline["node_features"]
        global_base = baseline["global_features"]
        steps = max(1, self.config.gradient_shap_steps)
        node_grad_acc = torch.zeros_like(node)
        global_grad_acc = torch.zeros_like(global_)

        for step in range(1, steps + 1):
            alpha = step / steps
            interp_node = (node_base + alpha * (node - node_base)).detach()
            interp_global = (global_base + alpha * (global_ - global_base)).detach()
            interp_node.requires_grad_(True)
            interp_global.requires_grad_(True)

            score = forward(interp_node, interp_global)
            score.backward()

            if interp_node.grad is not None:
                node_grad_acc += interp_node.grad.detach()
            if interp_global.grad is not None:
                global_grad_acc += interp_global.grad.detach()

        node_attr = (node - node_base) * node_grad_acc / steps
        global_attr = (global_ - global_base) * global_grad_acc / steps
        return node_attr.detach(), global_attr.detach()

    def _aggregate_coalitions(
        self,
        node_attr: Tensor,
        global_attr: Tensor,
        *,
        task: TaskName,
        region_index: int | None,
    ) -> GroupedShapValues:
        group_ids = coalition_ids_for_task(task)
        phi_values: list[float] = []

        for group_id in group_ids:
            if group_id in NODE_FEATURE_GROUPS:
                mask = node_coalition_mask(group_id, device=node_attr.device)
                if region_index is not None:
                    region_slice = node_attr[:, region_index, :]
                    value = float(region_slice[:, mask].sum().item())
                else:
                    value = float(node_attr[:, :, mask].sum().item())
            elif group_id in GLOBAL_FEATURE_GROUPS:
                mask = global_coalition_mask(group_id, device=global_attr.device)
                value = float(global_attr[:, mask].sum().item())
            else:
                value = 0.0
            phi_values.append(value)

        return GroupedShapValues(
            group_ids=group_ids,
            phi=np.asarray(phi_values, dtype=np.float64),
            task=task,
            region_index=region_index,
        )

    @staticmethod
    def _select_batch_index(batch: dict[str, Tensor], index: int) -> dict[str, Tensor]:
        node = batch["node_features"]
        global_ = batch["global_features"]
        if node.ndim == 4:
            sample = {
                "node_features": node[index],
                "global_features": global_[index],
                "adjacency": batch["adjacency"],
            }
            if "attention_bias" in batch:
                sample["attention_bias"] = batch["attention_bias"]
            return sample
        return batch

    @staticmethod
    def _zero_baseline(sample: dict[str, Tensor]) -> dict[str, Tensor]:
        return {
            "node_features": torch.zeros_like(sample["node_features"]),
            "global_features": torch.zeros_like(sample["global_features"]),
        }
