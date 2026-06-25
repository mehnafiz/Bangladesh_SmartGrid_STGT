"""Regional node-level attribution (Phase 12 L2)."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from constants import REGIONS
from explainability.attention_extractor import AttentionExtractor
from explainability.coalitions import NODE_LOCAL_GROUPS, NODE_FEATURE_GROUPS
from explainability.types import GroupedShapValues, NodeAttributionResult, NodeImportanceRow, SpatialAttentionResult
from utils.logging import get_logger

logger = get_logger(__name__)

DHAKA_INDEX = REGIONS.index("Dhaka")


class NodeAttributor:
    """
    Combine SHAP node coalition mass with spatial attention inflow/outflow.

    Always surfaces Dhaka separately per Phase 12 node importance design.
    """

    def __init__(self, attention_extractor: AttentionExtractor | None = None) -> None:
        self.attention_extractor = attention_extractor or AttentionExtractor()

    def compute(
        self,
        node_attributions: np.ndarray,
        spatial: SpatialAttentionResult,
        *,
        demand_shares: np.ndarray | None = None,
        dhaka_index: int = DHAKA_INDEX,
    ) -> NodeAttributionResult:
        """
        Rank nodes by combined attribution signals.

        Args:
            node_attributions: (T, N, F_n) integrated-gradient attributions
            spatial: aggregated spatial attention result
            demand_shares: optional (N,) regional demand share context
        """
        if node_attributions.ndim != 3:
            raise ValueError(
                f"node_attributions must be (T, N, F_n), got {node_attributions.shape}"
            )

        shap_mass = self._node_shap_mass(node_attributions)
        inflow, outflow = self.attention_extractor.spatial_inflow_outflow(
            spatial.influence_matrix
        )
        total_mass = float(np.sum(shap_mass))
        rows: list[NodeImportanceRow] = []

        for idx, region in enumerate(REGIONS):
            share = float(demand_shares[idx]) if demand_shares is not None else None
            contribution = float(shap_mass[idx] / total_mass) if total_mass > 0 else 0.0
            rows.append(
                NodeImportanceRow(
                    node=region,
                    shap_mass=float(shap_mass[idx]),
                    attention_inflow=float(inflow[idx]),
                    attention_outflow=float(outflow[idx]),
                    demand_share=share,
                    contribution=contribution,
                )
            )

        rows.sort(key=lambda row: row.shap_mass, reverse=True)
        logger.info(
            "Node attribution ranked top node=%s shap_mass=%.4f",
            rows[0].node,
            rows[0].shap_mass,
        )
        return NodeAttributionResult(rows=tuple(rows), dhaka_index=dhaka_index)

    def dhaka_row(self, result: NodeAttributionResult) -> NodeImportanceRow:
        for row in result.rows:
            if row.node == "Dhaka":
                return row
        raise ValueError("Dhaka not found in node attribution rows")

    def compare_share_vs_contribution(
        self,
        result: NodeAttributionResult,
    ) -> float:
        """Spearman ρ between demand share and SHAP contribution fractions."""
        from scipy.stats import spearmanr

        shares = [row.demand_share for row in result.rows if row.demand_share is not None]
        contribs = [row.contribution for row in result.rows if row.contribution is not None]
        if len(shares) < 2 or len(contribs) < 2:
            return 0.0
        rho, _ = spearmanr(shares, contribs)
        if np.isnan(rho):
            return 0.0
        return float(rho)

    def save_csv(self, result: NodeAttributionResult, path: Path, *, date_label: str = "") -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            "node,shap_mass,attention_inflow,attention_outflow,demand_share,contribution,date"
        ]
        for row in sorted(result.rows, key=lambda item: item.node):
            share = "" if row.demand_share is None else f"{row.demand_share:.6f}"
            contrib = "" if row.contribution is None else f"{row.contribution:.6f}"
            lines.append(
                f"{row.node},{row.shap_mass:.8f},{row.attention_inflow:.8f},"
                f"{row.attention_outflow:.8f},{share},{contrib},{date_label}"
            )
        path.write_text("\n".join(lines))
        logger.info("Saved node attribution CSV -> %s", path)
        return path

    @staticmethod
    def _node_shap_mass(node_attributions: np.ndarray) -> np.ndarray:
        feat_mask = np.zeros(node_attributions.shape[-1], dtype=bool)
        for group_id in NODE_LOCAL_GROUPS:
            for feat_idx in NODE_FEATURE_GROUPS[group_id]:
                feat_mask[feat_idx] = True
        masked = np.abs(node_attributions[:, :, feat_mask])
        return masked.sum(axis=(0, 2))

    @staticmethod
    def from_grouped_shap(grouped: GroupedShapValues) -> dict[str, float]:
        """Map grouped SHAP to approximate node masses when raw attributions unavailable."""
        mapping: dict[str, float] = {}
        for gid, phi in zip(grouped.group_ids, grouped.phi, strict=True):
            if gid in NODE_LOCAL_GROUPS:
                mapping[gid] = abs(float(phi))
        return mapping
