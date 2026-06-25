"""Tests for node, temporal, and stress attribution."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import torch

from constants import INPUT_WINDOW_T, N_NODES, NODE_FEATURES_PER_REGION, REGIONS
from explainability.attention_extractor import AttentionExtractor
from explainability.node_attribution import NodeAttributor
from explainability.shap_engine import ShapEngine
from explainability.stress_attribution import StressAttributor
from explainability.temporal_attribution import TemporalAttributor
from explainability.types import GroupedShapValues
from models.pf_stgt import PFSTGT
from targets.osi import OSIComponentBounds


def test_node_attribution_ranking() -> None:
    node_attr = np.random.randn(INPUT_WINDOW_T, N_NODES, NODE_FEATURES_PER_REGION)
    adj = np.ones((N_NODES, N_NODES)) / N_NODES
    spatial = AttentionExtractor().extract_spatial(torch.tensor(adj).unsqueeze(0).unsqueeze(0))
    shares = np.linspace(0.05, 0.2, N_NODES)
    result = NodeAttributor().compute(node_attr, spatial, demand_shares=shares)
    assert len(result.rows) == N_NODES
    assert result.dhaka_index == REGIONS.index("Dhaka")
    assert NodeAttributor().dhaka_row(result).node == "Dhaka"


def test_temporal_attribution_top_k() -> None:
    alpha = np.array([0.05, 0.1, 0.15, 0.2, 0.1, 0.2, 0.2])
    from explainability.types import TemporalAttentionResult

    temporal = TemporalAttributor(config=None).from_attention(
        TemporalAttentionResult(alpha_t=alpha / alpha.sum())
    )
    assert len(temporal.top_k_indices) == 3
    assert temporal.top_k_weights[0] >= temporal.top_k_weights[-1]


def test_stress_attribution_pathways() -> None:
    grouped = GroupedShapValues(
        group_ids=("G7", "G8", "G11"),
        phi=np.array([0.2, 0.5, 0.1]),
        task="stress",
    )
    components_bounds = OSIComponentBounds(
        c1=(0.0, 2.0),
        c2=(0.0, 1.0),
        c3=(0.0, 0.5),
    )
    row = pd.DataFrame(
        {
            **{f"{r}_demand": [1000.0] for r in REGIONS},
            **{f"{r}_load": [1100.0] for r in REGIONS},
            "Max. Demand at eve. peak (Generation end)": [9000.0],
            "Highest Generation (Generation end)": [10000.0],
            "Gas/LF limitation": [100.0],
            "Coal supply Limitation": [50.0],
            "Low water level in Kaptai lake": [0.0],
            "Plants under shut down/ maintenance": [200.0],
        }
    )
    attributor = StressAttributor()
    components = attributor.decompose_components(row, components_bounds)
    result = attributor.analyze(grouped, components)
    assert result.top_shap_group == "G8"
    assert components.driver in {"c1_shedding", "c2_reserve", "c3_limitation"}


def test_export_helpers(tmp_path: Path) -> None:
    grouped = GroupedShapValues(
        group_ids=("G7", "G8"),
        phi=np.array([0.1, 0.2]),
        task="stress",
    )
    engine = ShapEngine(PFSTGT())
    csv_path = engine.save_grouped_csv(grouped, tmp_path / "stress.csv")
    assert csv_path.exists()
    plot_path = engine.save_summary_plot(grouped, tmp_path / "summary.png")
    assert plot_path is not None
