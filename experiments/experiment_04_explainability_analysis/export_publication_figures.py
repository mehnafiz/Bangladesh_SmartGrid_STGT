#!/usr/bin/env python3
"""Export publication-quality explainability figures from verified model outputs.

Reads ONLY real artefacts produced by run_explainability.py:
  - results/explainability/shap/*.csv
  - results/explainability/attention/mean_spatial_matrix.csv
  - experiments/experiment_04_explainability_analysis/xai_metrics.json
  - results/explainability/case_studies/<date>/*.csv

No synthetic values. No PNG matrix extraction.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
PKG = ROOT / "paper" / "final_results_package"
EXP04 = Path(__file__).resolve().parent
RESULTS = ROOT / "results" / "explainability"
FIG_OUT = RESULTS / "figures"
METRICS = EXP04 / "xai_metrics.json"

if str(PKG) not in sys.path:
    sys.path.insert(0, str(PKG))

from ieee_design import (  # noqa: E402
    IEEE_ACCENT,
    IEEE_BLUE,
    IEEE_DARK,
    IEEE_GRAY,
    IEEE_GREEN,
    IEEE_LIGHT_BLUE,
    IEEE_RED,
    apply_rc,
    export_triple,
    heatmap_cmap_contrast,
)

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

LOCAL_CASE_DATE = "2024-09-08"


def _read_shap_csv(path: Path) -> tuple[tuple[str, ...], np.ndarray]:
    rows = list(csv.DictReader(path.open()))
    gids = tuple(r["group_id"] for r in rows)
    phi = np.array([float(r["phi"]) for r in rows], dtype=np.float64)
    return gids, phi


def _load_mean_spatial(metrics: dict) -> np.ndarray:
    csv_path = RESULTS / "attention" / "mean_spatial_matrix.csv"
    if csv_path.exists():
        data = np.genfromtxt(csv_path, delimiter=",", skip_header=1, usecols=range(1, 10))
        return np.asarray(data, dtype=np.float64)
    if "mean_spatial" in metrics:
        return np.array(metrics["mean_spatial"], dtype=np.float64)
    raise FileNotFoundError(
        "mean_spatial matrix missing. Run run_explainability.py first."
    )


def _bar_abs(gids, phi, title: str, stem: Path, *, highlight: set[str] | None = None) -> None:
    apply_rc()
    highlight = highlight or set()
    colors = [IEEE_GREEN if g in highlight else IEEE_ACCENT for g in gids]
    fig, ax = plt.subplots(figsize=(10, 4.2))
    ax.bar(list(gids), np.abs(phi), color=colors, edgecolor=IEEE_DARK, linewidth=0.5, width=0.72)
    ax.set_title(title, fontweight="bold")
    ax.set_ylabel("|φ| (mean absolute attribution)")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    export_triple(fig, stem)
    plt.close(fig)


def _bar_signed(gids, phi, title: str, stem: Path) -> None:
    apply_rc()
    colors = [IEEE_GREEN if v >= 0 else IEEE_RED for v in phi]
    fig, ax = plt.subplots(figsize=(10, 4.2))
    ax.bar(list(gids), phi, color=colors, edgecolor=IEEE_DARK, linewidth=0.5, width=0.72)
    ax.axhline(0, color=IEEE_DARK, linewidth=0.8)
    ax.set_title(title, fontweight="bold")
    ax.set_ylabel("φ (signed attribution)")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    export_triple(fig, stem)
    plt.close(fig)


def _node_attribution_bar(node_mass: dict[str, float], stem: Path) -> None:
    apply_rc()
    regions = list(REGIONS)
    values = np.array([node_mass[r] for r in regions], dtype=np.float64)
    order = np.argsort(values)[::-1]
    fig, ax = plt.subplots(figsize=(9, 4.2))
    colors = [IEEE_GREEN if regions[i] == "Dhaka" else IEEE_ACCENT for i in order]
    ax.bar([regions[i] for i in order], values[order], color=colors, edgecolor=IEEE_DARK, linewidth=0.5)
    ax.set_title("Regional node SHAP mass (averaged case studies)", fontweight="bold")
    ax.set_ylabel("mean |SHAP| mass")
    ax.tick_params(axis="x", rotation=45)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    export_triple(fig, stem)
    plt.close(fig)


def _temporal_bar(alpha: np.ndarray, stem: Path, *, window: int = 7) -> None:
    apply_rc()
    labels = [f"t-{window - 1 - i}" for i in range(len(alpha))]
    fig, ax = plt.subplots(figsize=(7.5, 3.2))
    ax.bar(labels, alpha, color=IEEE_BLUE, edgecolor=IEEE_DARK, linewidth=0.5, width=0.68)
    ax.set_title("Temporal attention attribution α_t", fontweight="bold")
    ax.set_ylabel("weight")
    ax.set_ylim(0, max(alpha) * 1.2)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    export_triple(fig, stem)
    plt.close(fig)


def _attention_heatmap(matrix: np.ndarray, rho: float, stem: Path) -> None:
    from matplotlib.colors import PowerNorm

    apply_rc()
    display = matrix.astype(np.float64).copy()
    np.fill_diagonal(display, np.nan)

    off_diag = matrix[~np.eye(matrix.shape[0], dtype=bool)]
    vmax = float(np.max(off_diag))

    cmap = heatmap_cmap_contrast().copy()
    cmap.set_bad(color="#edf2f7")

    fig, ax = plt.subplots(figsize=(7.4, 6.4))
    im = ax.imshow(
        display,
        cmap=cmap,
        norm=PowerNorm(gamma=0.55, vmin=0.0, vmax=vmax),
        aspect="equal",
    )
    ax.set_xticks(range(len(REGIONS)), REGIONS, rotation=45, ha="right", fontsize=9)
    ax.set_yticks(range(len(REGIONS)), REGIONS, fontsize=9)
    ax.set_title("Mean spatial attention influence (case studies)", fontweight="bold", fontsize=11)

    ax.set_xticks(np.arange(-0.5, len(REGIONS), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(REGIONS), 1), minor=True)
    ax.grid(which="minor", color="white", linestyle="-", linewidth=1.2)
    ax.tick_params(which="minor", bottom=False, left=False)

    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("attention weight", fontsize=8)
    cbar.ax.tick_params(labelsize=8)
    ax.text(
        0.98,
        0.02,
        f"ρ(attn, adj) = {rho:.3f}",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=8,
        color=IEEE_GRAY,
        bbox=dict(boxstyle="round,pad=0.2", facecolor=IEEE_LIGHT_BLUE, edgecolor=IEEE_BLUE, linewidth=0.5),
    )
    fig.tight_layout()
    export_triple(fig, stem)
    plt.close(fig)


def _stress_dual(components: dict[str, float], gids, phi: np.ndarray, stem: Path) -> None:
    apply_rc()
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2))
    comp_names = list(components.keys())
    comp_vals = list(components.values())
    axes[0].bar(comp_names, comp_vals, color=[IEEE_GREEN, IEEE_ACCENT, IEEE_RED], edgecolor=IEEE_DARK, linewidth=0.5)
    axes[0].set_title("OSI component norms (t+1)", fontweight="bold")
    axes[0].set_ylim(0, 1.05)
    axes[0].spines["top"].set_visible(False)
    axes[0].spines["right"].set_visible(False)

    axes[1].bar(list(gids), np.abs(phi), color=IEEE_BLUE, edgecolor=IEEE_DARK, linewidth=0.5)
    axes[1].set_title("Stress SHAP |φ| by coalition", fontweight="bold")
    axes[1].tick_params(axis="x", rotation=45)
    axes[1].spines["top"].set_visible(False)
    axes[1].spines["right"].set_visible(False)
    fig.tight_layout()
    export_triple(fig, stem)
    plt.close(fig)


def _local_explanation(case_date: str, stem: Path) -> None:
    case_dir = RESULTS / "case_studies" / case_date
    if not case_dir.exists():
        raise FileNotFoundError(f"Case study directory missing: {case_dir}")

    stress_gids, stress_phi = _read_shap_csv(case_dir / "stress_shap.csv")
    node_rows = list(csv.DictReader((case_dir / "node_importance.csv").open()))
    alpha_rows = list(csv.DictReader((case_dir / "temporal_alpha.csv").open()))
    comp_rows = {r["component"]: float(r["normalized"]) for r in csv.DictReader((case_dir / "osi_components.csv").open())}

    nodes = [r["node"] for r in node_rows]
    node_mass = np.array([float(r["shap_mass"]) for r in node_rows], dtype=np.float64)
    alpha = np.array([float(r["alpha_t"]) for r in alpha_rows], dtype=np.float64)
    labels = [f"t-{6 - i}" for i in range(len(alpha))]

    apply_rc()
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    fig.suptitle(f"Local explanation — {case_date} (high-stress test case)", fontweight="bold", fontsize=12)

    colors = [IEEE_GREEN if v >= 0 else IEEE_RED for v in stress_phi]
    axes[0, 0].bar(list(stress_gids), stress_phi, color=colors, edgecolor=IEEE_DARK, linewidth=0.5)
    axes[0, 0].axhline(0, color=IEEE_DARK, linewidth=0.6)
    axes[0, 0].set_title("Stress SHAP (signed φ)")
    axes[0, 0].tick_params(axis="x", rotation=45)

    comp_names = list(comp_rows.keys())
    axes[0, 1].bar(comp_names, list(comp_rows.values()), color=[IEEE_GREEN, IEEE_ACCENT, IEEE_RED], edgecolor=IEEE_DARK, linewidth=0.5)
    axes[0, 1].set_title("OSI components (normalized)")
    axes[0, 1].set_ylim(0, 1.05)

    order = np.argsort(node_mass)[::-1]
    bar_colors = [IEEE_GREEN if nodes[i] == "Dhaka" else IEEE_ACCENT for i in order]
    axes[1, 0].bar([nodes[i] for i in order], node_mass[order], color=bar_colors, edgecolor=IEEE_DARK, linewidth=0.5)
    axes[1, 0].set_title("Node SHAP mass")
    axes[1, 0].tick_params(axis="x", rotation=45)

    axes[1, 1].bar(labels, alpha, color=IEEE_BLUE, edgecolor=IEEE_DARK, linewidth=0.5)
    axes[1, 1].set_title("Temporal α_t")

    for ax in axes.flat:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    fig.tight_layout()
    export_triple(fig, stem)
    plt.close(fig)


def main() -> None:
    if not METRICS.exists():
        raise FileNotFoundError(f"Missing {METRICS}. Run run_explainability.py first.")

    metrics = json.loads(METRICS.read_text())
    FIG_OUT.mkdir(parents=True, exist_ok=True)

    stress_gids, stress_phi = _read_shap_csv(RESULTS / "shap" / "global_stress.csv")
    demand_gids, demand_phi = _read_shap_csv(RESULTS / "shap" / "global_demand_dhaka.csv")
    mean_spatial = _load_mean_spatial(metrics)
    mean_temporal = np.array(metrics["mean_temporal_alpha"], dtype=np.float64)
    rho = float(metrics["attention_adjacency_spearman"])
    node_mass = metrics["node_mass_mean"]

    case_date = LOCAL_CASE_DATE
    for c in metrics.get("cases", []):
        if c.get("stratum") == "high_stress" and c.get("split") == "test":
            case_date = c["date"]
            break

    rep_dir = RESULTS / "case_studies" / case_date
    rep_gids, rep_phi = _read_shap_csv(rep_dir / "stress_shap.csv")
    comp_rows = {
        r["component"]: float(r["normalized"])
        for r in csv.DictReader((rep_dir / "osi_components.csv").open())
    }

    generated: list[str] = []

    _bar_abs(
        demand_gids,
        demand_phi,
        "Global demand SHAP — Dhaka (|φ|)",
        FIG_OUT / "01_shap_summary_demand",
        highlight={"G6", "G4", "G10"},
    )
    generated.append("01_shap_summary_demand")

    _bar_abs(
        stress_gids,
        stress_phi,
        "Global stress SHAP (|φ|)",
        FIG_OUT / "02_shap_summary_stress",
        highlight={"G8", "G6"},
    )
    generated.append("02_shap_summary_stress")

    _bar_signed(stress_gids, stress_phi, "Global stress SHAP (signed φ)", FIG_OUT / "03_shap_bar_stress")
    generated.append("03_shap_bar_stress")

    _node_attribution_bar(node_mass, FIG_OUT / "04_node_attribution")
    generated.append("04_node_attribution")

    _temporal_bar(mean_temporal, FIG_OUT / "05_temporal_attribution")
    generated.append("05_temporal_attribution")

    _attention_heatmap(mean_spatial, rho, FIG_OUT / "06_attention_heatmap")
    generated.append("06_attention_heatmap")

    _stress_dual(
        {"c1": comp_rows["c1"], "c2": comp_rows["c2"], "c3": comp_rows["c3"]},
        rep_gids,
        rep_phi,
        FIG_OUT / "07_stress_attribution",
    )
    generated.append("07_stress_attribution")

    _local_explanation(case_date, FIG_OUT / f"08_local_explanation_{case_date}")
    generated.append(f"08_local_explanation_{case_date}")

    manifest = {
        "checkpoint": metrics.get("checkpoint"),
        "device": metrics.get("device"),
        "local_case": case_date,
        "figures": [f"{name}.{{pdf,svg,png}}" for name in generated],
        "source_artefacts": [
            str(RESULTS / "shap" / "global_stress.csv"),
            str(RESULTS / "shap" / "global_demand_dhaka.csv"),
            str(RESULTS / "attention" / "mean_spatial_matrix.csv"),
            str(METRICS),
            str(rep_dir),
        ],
    }
    (FIG_OUT / "manifest.json").write_text(json.dumps(manifest, indent=2))

    print(f"Exported {len(generated)} real explainability figure sets -> {FIG_OUT}")
    for name in generated:
        print(f"  {name}.pdf / .svg / .png")


if __name__ == "__main__":
    main()
