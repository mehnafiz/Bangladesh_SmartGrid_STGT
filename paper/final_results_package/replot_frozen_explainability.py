#!/usr/bin/env python3
"""Replot Exp04 manuscript figures from frozen CSV/JSON/PNG only (no model inference)."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from ieee_design import (
    ANNOT_SIZE,
    BAR_EDGE_LW,
    COALITION_ORDER,
    IEEE_ACCENT,
    IEEE_BLUE,
    IEEE_DARK,
    IEEE_GRAY,
    IEEE_GREEN,
    IEEE_LIGHT_BLUE,
    IEEE_RED,
    LABEL_SIZE,
    TICK_SIZE,
    TITLE_SIZE,
    apply_rc,
    coalition_tick_labels,
    export_triple,
    heatmap_cmap_contrast,
    style_bar_axes,
)

ROOT = Path(__file__).resolve().parents[2]
PKG = Path(__file__).resolve().parent
FIG = PKG / "figures"
EXP04 = ROOT / "experiments/experiment_04_explainability_analysis"
METRICS = EXP04 / "xai_metrics.json"
SHAP_DIR = ROOT / "results/explainability/shap"
CASE_HIGH_STRESS = ROOT / "results/explainability/case_studies/2024-09-08"
SPATIAL_CSV = ROOT / "results/explainability/attention/mean_spatial_matrix.csv"

REGIONS = (
    "Barishal",
    "Chattogram",
    "Cumilla",
    "Dhaka",
    "Khulna",
    "Mymensingh",
    "Rajshahi",
    "Rangpur",
    "Sylhet",
)

DEMAND_HIGHLIGHT = {"G4", "G6", "G10"}
STRESS_HIGHLIGHT = {"G6", "G8"}


def _read_shap_csv(path: Path) -> tuple[tuple[str, ...], np.ndarray, np.ndarray]:
    rows = list(csv.DictReader(path.open()))
    gids = tuple(r["group_id"] for r in rows)
    phi = np.array([float(r["phi"]) for r in rows], dtype=np.float64)
    return gids, phi, np.abs(phi)


def _coalition_values(
    group_ids: tuple[str, ...],
    phi: np.ndarray,
    *,
    absolute: bool = True,
) -> np.ndarray:
    lookup = {gid: float(v) for gid, v in zip(group_ids, phi, strict=True)}
    values = np.array([lookup.get(gid, np.nan) for gid in COALITION_ORDER], dtype=np.float64)
    if absolute:
        values = np.abs(values)
    return values


def _plot_dual_shap(
    demand_ids: tuple[str, ...],
    demand_phi: np.ndarray,
    stress_ids: tuple[str, ...],
    stress_phi: np.ndarray,
    path_stem: Path,
) -> None:
    """Publication dual-panel SHAP summary (demand + stress) from frozen CSVs."""
    apply_rc()
    demand_vals = _coalition_values(demand_ids, demand_phi)
    stress_vals = _coalition_values(stress_ids, stress_phi)
    stress_plot = np.ma.masked_invalid(stress_vals)
    x = np.arange(len(COALITION_ORDER))
    tick_labels = coalition_tick_labels()

    fig, axes = plt.subplots(2, 1, figsize=(10.4, 6.2), sharex=True)
    fig.subplots_adjust(hspace=0.30, top=0.96, bottom=0.14)

    demand_colors = [
        IEEE_GREEN if gid in DEMAND_HIGHLIGHT else IEEE_ACCENT for gid in COALITION_ORDER
    ]
    stress_colors = [
        IEEE_GREEN if gid in STRESS_HIGHLIGHT else IEEE_ACCENT for gid in COALITION_ORDER
    ]

    axes[0].bar(
        x,
        demand_vals,
        color=demand_colors,
        edgecolor=IEEE_DARK,
        linewidth=BAR_EDGE_LW,
        width=0.72,
    )
    axes[0].set_ylabel("|φ| (MW)", fontsize=LABEL_SIZE)
    axes[0].set_title("(a) Global SHAP summary — demand forecasting (Dhaka)", fontweight="bold", loc="left", fontsize=TITLE_SIZE)
    style_bar_axes(axes[0], grid_axis="y")

    axes[1].bar(
        x,
        stress_plot,
        color=stress_colors,
        edgecolor=IEEE_DARK,
        linewidth=BAR_EDGE_LW,
        width=0.72,
    )
    axes[1].set_ylabel("|φ|", fontsize=LABEL_SIZE)
    axes[1].set_title("(b) Global SHAP summary — operational stress forecasting", fontweight="bold", loc="left", fontsize=TITLE_SIZE)
    axes[1].set_xticks(x, tick_labels, fontsize=7.0)
    for lbl in axes[1].get_xticklabels():
        lbl.set_ha("center")
    style_bar_axes(axes[1], grid_axis="y")

    fig.tight_layout()
    export_triple(fig, path_stem)
    plt.close(fig)


def _plot_grouped_bar(
    group_ids: tuple[str, ...],
    phi: np.ndarray,
    title: str,
    path_stem: Path,
    *,
    highlight: set[str] | None = None,
) -> None:
    apply_rc()
    highlight = highlight or set()
    colors = [IEEE_GREEN if gid in highlight else IEEE_ACCENT for gid in group_ids]
    labels = coalition_tick_labels(group_ids)
    fig, ax = plt.subplots(figsize=(10.2, 4.4))
    ax.bar(range(len(group_ids)), phi, color=colors, edgecolor=IEEE_DARK, linewidth=BAR_EDGE_LW, width=0.72)
    ax.set_xticks(range(len(group_ids)), labels, fontsize=7.5)
    ax.set_title(title, fontweight="bold", fontsize=TITLE_SIZE)
    ax.set_ylabel("|φ| (mean absolute attribution)", fontsize=LABEL_SIZE)
    style_bar_axes(ax, grid_axis="y")
    export_triple(fig, path_stem)
    plt.close(fig)


def _plot_temporal(alpha_t: np.ndarray, path_stem: Path, *, window: int = 7) -> None:
    apply_rc()
    labels = [f"t−{window - 1 - i}" for i in range(len(alpha_t))]
    fig, ax = plt.subplots(figsize=(7.8, 3.4))
    ax.bar(labels, alpha_t, color=IEEE_BLUE, edgecolor=IEEE_DARK, linewidth=BAR_EDGE_LW, width=0.68)
    ax.set_title("Temporal attention attribution α_t", fontweight="bold", fontsize=TITLE_SIZE)
    ax.set_ylabel("weight", fontsize=LABEL_SIZE)
    ax.set_xlabel("lookback lag", fontsize=LABEL_SIZE)
    ax.set_ylim(0, max(alpha_t) * 1.2)
    style_bar_axes(ax, grid_axis="y")
    export_triple(fig, path_stem)
    plt.close(fig)


def _plot_stress_dual(
    components: dict[str, float],
    shap_groups: tuple[str, ...],
    shap_phi: np.ndarray,
    path_stem: Path,
) -> None:
    apply_rc()
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.4))
    comp_names = ["c1: shedding", "c2: reserve", "c3: limitation"]
    comp_vals = [components["c1"], components["c2"], components["c3"]]
    comp_colors = [IEEE_GREEN, IEEE_ACCENT, IEEE_RED]
    axes[0].bar(comp_names, comp_vals, color=comp_colors, edgecolor=IEEE_DARK, linewidth=BAR_EDGE_LW)
    axes[0].set_title("OSI component norms (t+1)", fontweight="bold", fontsize=TITLE_SIZE)
    axes[0].set_ylim(0, 1.05)
    style_bar_axes(axes[0], grid_axis="y")

    shap_labels = coalition_tick_labels(shap_groups)
    axes[1].bar(
        range(len(shap_groups)),
        np.abs(shap_phi),
        color=IEEE_BLUE,
        edgecolor=IEEE_DARK,
        linewidth=BAR_EDGE_LW,
    )
    axes[1].set_xticks(range(len(shap_groups)), shap_labels, fontsize=7.0)
    axes[1].set_title("Stress SHAP |φ| by coalition", fontweight="bold", fontsize=TITLE_SIZE)
    style_bar_axes(axes[1], grid_axis="y")
    fig.tight_layout()
    export_triple(fig, path_stem)
    plt.close(fig)


def _load_mean_spatial(metrics: dict) -> np.ndarray:
    """Load real 9×9 spatial attention matrix from Exp04 model outputs."""
    if SPATIAL_CSV.exists():
        return np.genfromtxt(SPATIAL_CSV, delimiter=",", skip_header=1, usecols=range(1, 10))
    if "mean_spatial" in metrics:
        return np.array(metrics["mean_spatial"], dtype=np.float64)
    raise FileNotFoundError(
        f"Missing {SPATIAL_CSV}. Run run_explainability.py before replotting Fig. 7."
    )


def _plot_node_heatmap(matrix: np.ndarray, rho: float, path_stem: Path) -> None:
    from matplotlib.colors import PowerNorm

    apply_rc()
    display = matrix.astype(np.float64).copy()
    np.fill_diagonal(display, np.nan)

    off_diag = matrix[~np.eye(matrix.shape[0], dtype=bool)]
    vmax = float(np.max(off_diag))

    cmap = heatmap_cmap_contrast().copy()
    cmap.set_bad(color="#edf2f7")

    fig, ax = plt.subplots(figsize=(7.2, 6.2))
    im = ax.imshow(
        display,
        cmap=cmap,
        norm=PowerNorm(gamma=0.55, vmin=0.0, vmax=vmax),
        aspect="equal",
    )
    ax.set_xticks(range(len(REGIONS)), REGIONS, rotation=45, ha="right", fontsize=TICK_SIZE)
    ax.set_yticks(range(len(REGIONS)), REGIONS, fontsize=TICK_SIZE)
    ax.set_xlabel("source division", fontsize=LABEL_SIZE)
    ax.set_ylabel("target division", fontsize=LABEL_SIZE)
    ax.set_title("Mean spatial attention influence (case studies)", fontweight="bold", fontsize=TITLE_SIZE)

    ax.set_xticks(np.arange(-0.5, len(REGIONS), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(REGIONS), 1), minor=True)
    ax.grid(which="minor", color="white", linestyle="-", linewidth=1.2)
    ax.tick_params(which="minor", bottom=False, left=False)

    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("attention weight", fontsize=ANNOT_SIZE)
    cbar.ax.tick_params(labelsize=ANNOT_SIZE)

    ax.text(
        0.98,
        0.02,
        f"ρ(attn, adj) = {rho:.3f}",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=ANNOT_SIZE,
        color=IEEE_GRAY,
        bbox=dict(boxstyle="round,pad=0.2", facecolor=IEEE_LIGHT_BLUE, edgecolor=IEEE_BLUE, linewidth=0.5),
    )
    fig.tight_layout()
    export_triple(fig, path_stem)
    plt.close(fig)


def main() -> None:
    FIG.mkdir(parents=True, exist_ok=True)

    stress_ids, stress_phi, stress_abs = _read_shap_csv(SHAP_DIR / "global_stress.csv")
    demand_ids, demand_phi, demand_abs = _read_shap_csv(SHAP_DIR / "global_demand_dhaka.csv")

    _plot_dual_shap(
        demand_ids,
        demand_phi,
        stress_ids,
        stress_phi,
        FIG / "figure_06_dual_shap",
    )
    _plot_grouped_bar(
        stress_ids,
        stress_abs,
        "Global stress SHAP (|φ|)",
        FIG / "figure_06_shap_summary_stress",
        highlight=STRESS_HIGHLIGHT,
    )
    _plot_grouped_bar(
        demand_ids,
        demand_abs,
        "Global demand SHAP — Dhaka (|φ|)",
        FIG / "figure_06_shap_summary_demand",
        highlight=DEMAND_HIGHLIGHT,
    )

    metrics = json.loads(METRICS.read_text())
    alpha = np.array(metrics["mean_temporal_alpha"], dtype=np.float64)
    _plot_temporal(alpha, FIG / "figure_08_temporal_attribution")

    comp_rows = {
        r["component"]: float(r["normalized"])
        for r in csv.DictReader((CASE_HIGH_STRESS / "osi_components.csv").open())
    }
    shap_ids, shap_phi, _ = _read_shap_csv(CASE_HIGH_STRESS / "stress_shap.csv")
    _plot_stress_dual(
        {"c1": comp_rows["c1"], "c2": comp_rows["c2"], "c3": comp_rows["c3"]},
        shap_ids,
        shap_phi,
        FIG / "figure_09_stress_attribution",
    )

    matrix = _load_mean_spatial(metrics)
    rho = float(metrics["attention_adjacency_spearman"])
    _plot_node_heatmap(matrix, rho, FIG / "figure_07_node_importance")

    print(f"Replotted frozen explainability figures -> {FIG}")


if __name__ == "__main__":
    main()
