#!/usr/bin/env python3
"""Stage 05B — assemble publication figures from frozen experiment outputs only."""

from __future__ import annotations

import csv
import shutil
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
PKG = Path(__file__).resolve().parent
FIG = PKG / "figures"

EXP02 = ROOT / "experiments/experiment_02_benchmark_models/benchmark_results.csv"
EXP03 = ROOT / "experiments/experiment_03_ablation_studies/ablation_results.csv"
EXP01_TRAIN = ROOT / "experiments/experiment_01_pf_stgt/train_loss.png"
EXP01_VAL = ROOT / "experiments/experiment_01_pf_stgt/val_loss.png"
EXP04_FIG = ROOT / "experiments/experiment_04_explainability_analysis/figures"


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def figure_01_framework() -> None:
    fig, ax = plt.subplots(figsize=(11, 6.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    ax.set_title("PF-STGT Multi-Task Forecasting Framework", fontsize=14, fontweight="bold", pad=12)

    boxes = [
        (0.4, 4.6, 2.2, 0.9, "Regional node features\n(B, T=7, N=9, F=9)"),
        (0.4, 3.3, 2.2, 0.9, "Global context\n(B, T=7, F=17)"),
        (0.4, 2.0, 2.2, 0.9, "Graph adjacency\n(N, N)"),
        (3.2, 3.8, 2.4, 1.2, "Embedding +\nPositional Encoding"),
        (6.0, 4.6, 2.3, 0.9, "Graph Transformer\n(spatial attention)"),
        (6.0, 3.3, 2.3, 0.9, "Temporal Transformer\n(lag attention)"),
        (6.0, 2.0, 2.3, 0.9, "Gated Parallel Fusion"),
        (8.8, 4.2, 1.0, 0.8, "Demand\nHead (9 MW)"),
        (8.8, 2.4, 1.0, 0.8, "Stress\nHead (OSI)"),
    ]
    for x, y, w, h, text in boxes:
        patch = FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.03",
            linewidth=1.2,
            edgecolor="#2c5282",
            facecolor="#ebf8ff",
        )
        ax.add_patch(patch)
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=8.5)

    arrows = [
        ((2.6, 5.05), (3.2, 4.4)),
        ((2.6, 3.75), (3.2, 4.2)),
        ((2.6, 2.45), (3.2, 3.9)),
        ((5.6, 4.4), (6.0, 5.05)),
        ((5.6, 4.2), (6.0, 3.75)),
        ((5.6, 3.9), (6.0, 2.45)),
        ((8.3, 4.4), (8.8, 4.6)),
        ((8.3, 2.45), (8.8, 2.8)),
    ]
    for start, end in arrows:
        ax.add_patch(
            FancyArrowPatch(start, end, arrowstyle="->", mutation_scale=12, color="#4a5568", lw=1.0)
        )

    ax.text(
        5.0,
        0.35,
        "Final model S2: correlation graph (τ=0.65); geographical hybrid removed",
        ha="center",
        fontsize=9,
        style="italic",
        color="#2d3748",
    )
    fig.tight_layout()
    fig.savefig(FIG / "figure_01_framework.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def figure_02_s2_architecture() -> None:
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis("off")
    ax.set_title("S2 — Correlation-Only PF-STGT (Final Architecture)", fontsize=14, fontweight="bold", pad=12)

    s1 = FancyBboxPatch(
        (0.5, 3.6),
        4.0,
        1.0,
        boxstyle="round,pad=0.03",
        linewidth=1.2,
        edgecolor="#c53030",
        facecolor="#fff5f5",
    )
    s2 = FancyBboxPatch(
        (5.5, 3.6),
        4.0,
        1.0,
        boxstyle="round,pad=0.03",
        linewidth=1.2,
        edgecolor="#276749",
        facecolor="#f0fff4",
    )
    ax.add_patch(s1)
    ax.add_patch(s2)
    ax.text(2.5, 4.1, "S1 (superseded)\nHybrid geo + corr graph", ha="center", va="center", fontsize=9)
    ax.text(7.5, 4.1, "S2 (final)\nCorrelation graph only", ha="center", va="center", fontsize=9, fontweight="bold")

    shared = [
        (1.0, 2.2, 8.0, 0.9, "Shared trunk: PFSTGT — Graph + Temporal transformers + Fusion (749,058 params)"),
        (1.0, 1.0, 3.8, 0.9, "Multi-task loss\nHuber/100 + 20·MSE(OSI)"),
        (5.2, 1.0, 3.8, 0.9, "Test demand MAE: 88.65 MW\nStress R²: 0.745"),
    ]
    for x, y, w, h, text in shared:
        patch = FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.03",
            linewidth=1.0,
            edgecolor="#2c5282",
            facecolor="#ebf8ff",
        )
        ax.add_patch(patch)
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=9)

    ax.annotate(
        "",
        xy=(5.5, 4.1),
        xytext=(4.5, 4.1),
        arrowprops=dict(arrowstyle="->", color="#276749", lw=2),
    )
    ax.text(5.0, 4.35, "−4.66 MW", ha="center", fontsize=8, color="#276749")

    fig.tight_layout()
    fig.savefig(FIG / "figure_02_s2_architecture.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def figure_03_training_curves() -> None:
    train = Image.open(EXP01_TRAIN)
    val = Image.open(EXP01_VAL)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    axes[0].imshow(train)
    axes[0].set_title("Training loss (Exp01 W20 reference)", fontsize=11)
    axes[0].axis("off")
    axes[1].imshow(val)
    axes[1].set_title("Validation loss (Exp01 W20 reference)", fontsize=11)
    axes[1].axis("off")
    fig.suptitle("Figure 3 — Training Curves (frozen historical run)", fontsize=13, fontweight="bold")
    fig.tight_layout()
    fig.savefig(FIG / "figure_03_training_curves.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def figure_04_benchmark_comparison() -> None:
    rows = _read_csv(EXP02)
    order = ["B02", "B03", "B07", "S2", "B06"]
    labels_map = {
        "B02": "Random Forest",
        "B03": "XGBoost",
        "B07": "PF-STGT (S1)",
        "S2": "PF-STGT (S2) ★",
        "B06": "T-GCN",
    }
    by_id = {r["benchmark_id"]: r for r in rows}
    values: list[tuple[str, float]] = []
    for bid in order:
        if bid == "S2":
            values.append((labels_map[bid], 88.64871215820312))
        else:
            values.append((labels_map[bid], float(by_id[bid]["demand_mae"])))

    labels = [v[0] for v in values]
    maes = [v[1] for v in values]
    colors = ["#3182ce" if "S2" not in lb else "#276749" for lb in labels]

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.barh(labels, maes, color=colors, edgecolor="#1a202c", linewidth=0.6)
    ax.set_xlabel("Test demand MAE (MW)")
    ax.set_title("Benchmark Comparison — Demand Forecasting (test set)", fontweight="bold")
    ax.invert_yaxis()
    for bar, mae in zip(bars, maes):
        ax.text(mae + 2, bar.get_y() + bar.get_height() / 2, f"{mae:.1f}", va="center", fontsize=9)
    ax.set_xlim(0, max(maes) * 1.15)
    fig.tight_layout()
    fig.savefig(FIG / "figure_04_benchmark_comparison.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def figure_05_ablation_comparison() -> None:
    rows = _read_csv(EXP03)
    order = ["A4", "A6", "A3", "A1", "A2", "A5"]
    name_map = {
        "A1": "A1 PF-STGT (S1 ref)",
        "A2": "A2 No Graph",
        "A3": "A3 No Transformer",
        "A4": "A4 Single-Task",
        "A5": "A5 Geo Graph Only",
        "A6": "A6 Corr Graph (S2) ★",
    }
    by_id = {r["ablation_id"]: r for r in rows}
    labels = [name_map[i] for i in order]
    maes = [float(by_id[i]["demand_mae"]) for i in order]
    colors = ["#276749" if i == "A6" else "#805ad5" if i == "A4" else "#718096" for i in order]

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.barh(labels, maes, color=colors, edgecolor="#1a202c", linewidth=0.6)
    ax.set_xlabel("Test demand MAE (MW)")
    ax.set_title("Ablation Study — Demand MAE (test set)", fontweight="bold")
    ax.invert_yaxis()
    for bar, mae in zip(bars, maes):
        ax.text(mae + 1.5, bar.get_y() + bar.get_height() / 2, f"{mae:.1f}", va="center", fontsize=9)
    fig.tight_layout()
    fig.savefig(FIG / "figure_05_ablation_comparison.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def copy_explainability_figures() -> None:
    mapping = {
        "figure_shap_summary_stress.png": "figure_06_shap_summary_stress.png",
        "figure_shap_summary_demand.png": "figure_06_shap_summary_demand.png",
        "figure_node_importance_heatmap.png": "figure_07_node_importance.png",
        "figure_temporal_importance.png": "figure_08_temporal_attribution.png",
        "figure_stress_attribution.png": "figure_09_stress_attribution.png",
    }
    for src_name, dst_name in mapping.items():
        shutil.copy2(EXP04_FIG / src_name, FIG / dst_name)


def main() -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    figure_01_framework()
    figure_02_s2_architecture()
    figure_03_training_curves()
    figure_04_benchmark_comparison()
    figure_05_ablation_comparison()
    copy_explainability_figures()
    print(f"Publication figures written to {FIG}")


if __name__ == "__main__":
    main()
