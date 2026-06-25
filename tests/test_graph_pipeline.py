"""Tests for P3 graph pipeline."""

from __future__ import annotations

import numpy as np
import pytest

from constants import N_NODES
from data.loader import DataStore
from graph.adjacency import AdjacencyLoader, load_adjacency_matrix
from graph.bias import compute_attention_bias
from graph.pipeline import GraphPipeline
from graph.registry import GraphRegistry, GraphVariant


def test_hybrid_adjacency_shape_and_properties() -> None:
    adj = load_adjacency_matrix()
    assert adj.shape == (N_NODES, N_NODES)
    assert np.allclose(np.diag(adj), 0.0)
    assert (adj >= 0).all()


def test_attention_bias_masks_zero_edges() -> None:
    adj = load_adjacency_matrix()
    bias = compute_attention_bias(adj)
    zero_mask = adj == 0
    assert (bias[zero_mask] < -1e8).all()
    assert np.isfinite(bias[adj > 0]).all()


def test_graph_pipeline_builds_x_graph() -> None:
    result = GraphPipeline().build()
    assert result.x_graph.adjacency.shape == (N_NODES, N_NODES)
    assert result.x_graph.attention_bias.shape == (N_NODES, N_NODES)
    assert result.x_graph.variant == "hybrid"


def test_graph_registry_variants() -> None:
    store = DataStore(verify_md5=True)
    registry = GraphRegistry(train_clean=store.get_split("train").clean)
    hybrid = registry.get(GraphVariant.HYBRID)
    geo = registry.get(GraphVariant.GEO)
    corr = registry.get(GraphVariant.CORR)
    assert hybrid.shape == geo.shape == corr.shape == (N_NODES, N_NODES)
    assert (geo > 0).sum() <= (hybrid > 0).sum() <= (corr > 0).sum()
