#!/usr/bin/env python3
"""Replot Exp04 manuscript figures from frozen CSV/JSON only (no model inference)."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
PKG = Path(__file__).resolve().parent
FIG = PKG / "figures"
EXP04 = ROOT / "experiments/experiment_04_explainability_analysis"
METRICS = EXP04 / "xai_metrics.json"
SHAP_DIR = ROOT / "results/explainability/shap"
CASE_HIGH_STRESS = ROOT / "results/explainability/case_studies/2024-09-08"

PUBLICATION_DPI = 300

plt.rcParams.update(
    {
        "font.size": 11,
        "axes.titlesize": 12,
        "axes.labelsize": 11,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "savefig.dpi": PUBLICATION_DPI,
        "savefig.bbox": "tight",
        "figure.dpi": PUBLICATION_DPI,
    }
)


def _read_shap_csv(path: Path) -> tuple[tuple[str, ...], np.ndarray, np.ndarray]:
    rows = list(csv.DictReader(path.open()))
    gids = tuple(r["group_id"] for r in rows)
    phi = np.array([float(r["phi"]) for r in rows], dtype=np.float64)
    return gids, phi, np.abs(phi)


def _plot_grouped_bar(
    group_ids: tuple[str, ...],
    phi: np.ndarray,
    title: str,
    path: Path,
) -> None:
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(list(group_ids), phi, color="#2563eb", edgecolor="#1a202c", linewidth=0.4)
    ax.set_title(title)
    ax.set_ylabel("|φ| (mean absolute attribution)")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    fig.savefig(path, dpi=PUBLICATION_DPI, bbox_inches="tight")
    plt.close(fig)


def _plot_temporal(alpha_t: np.ndarray, path: Path, *, window: int = 7) -> None:
    labels = [f"t-{window - 1 - i}" for i in range(len(alpha_t))]
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.bar(labels, alpha_t, color="#7c3aed", edgecolor="#1a202c", linewidth=0.4)
    ax.set_title("Temporal attention attribution α_t")
    ax.set_ylabel("weight")
    fig.tight_layout()
    fig.savefig(path, dpi=PUBLICATION_DPI, bbox_inches="tight")
    plt.close(fig)


def _plot_stress_dual(
    components: dict[str, float],
    shap_groups: tuple[str, ...],
    shap_phi: np.ndarray,
    path: Path,
) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    comp_names = list(components.keys())
    comp_vals = list(components.values())
    axes[0].bar(comp_names, comp_vals, color="#ea580c", edgecolor="#1a202c", linewidth=0.4)
    axes[0].set_title("OSI component norms (t+1)")
    axes[0].set_ylim(0, 1.05)

    axes[1].bar(list(shap_groups), np.abs(shap_phi), color="#0891b2", edgecolor="#1a202c", linewidth=0.4)
    axes[1].set_title("Stress SHAP |φ| by coalition")
    axes[1].tick_params(axis="x", rotation=45)
    fig.tight_layout()
    fig.savefig(path, dpi=PUBLICATION_DPI, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    FIG.mkdir(parents=True, exist_ok=True)

    stress_ids, _, stress_abs = _read_shap_csv(SHAP_DIR / "global_stress.csv")
    demand_ids, _, demand_abs = _read_shap_csv(SHAP_DIR / "global_demand_dhaka.csv")

    _plot_grouped_bar(
        stress_ids,
        stress_abs,
        "Global stress SHAP (|φ|)",
        FIG / "figure_06_shap_summary_stress.png",
    )
    _plot_grouped_bar(
        demand_ids,
        demand_abs,
        "Global demand SHAP — Dhaka (|φ|)",
        FIG / "figure_06_shap_summary_demand.png",
    )

    metrics = json.loads(METRICS.read_text())
    alpha = np.array(metrics["mean_temporal_alpha"], dtype=np.float64)
    _plot_temporal(alpha, FIG / "figure_08_temporal_attribution.png")

    comp_rows = {r["component"]: float(r["normalized"]) for r in csv.DictReader((CASE_HIGH_STRESS / "osi_components.csv").open())}
    shap_ids, shap_phi, _ = _read_shap_csv(CASE_HIGH_STRESS / "stress_shap.csv")
    _plot_stress_dual(
        {"c1": comp_rows["c1"], "c2": comp_rows["c2"], "c3": comp_rows["c3"]},
        shap_ids,
        shap_phi,
        FIG / "figure_09_stress_attribution.png",
    )

    print(f"Replotted frozen explainability figures at {PUBLICATION_DPI} DPI -> {FIG}")


if __name__ == "__main__":
    main()
