#!/usr/bin/env python3
"""Stage 05B — assemble publication figures from frozen experiment outputs only."""

from __future__ import annotations

import csv
import shutil
import subprocess
import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

from ieee_design import (
    ARROW_LW,
    ARROW_LW_EMPHASIS,
    ARROW_MUTATION,
    ARROW_STYLE,
    BAR_EDGE_LW,
    BOX_LW,
    BOX_LW_HERO,
    IEEE_ACCENT,
    IEEE_BLUE,
    IEEE_DARK,
    IEEE_GRAY,
    IEEE_GREEN,
    IEEE_LIGHT_BLUE,
    IEEE_LIGHT_GREEN,
    IEEE_LIGHT_RED,
    IEEE_MUTED,
    IEEE_RED,
    LABEL_SIZE,
    SUBTITLE_SIZE,
    TICK_SIZE,
    TITLE_SIZE,
    apply_rc,
    export_triple,
    style_bar_axes,
)

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


def _draw_band(ax, x: float, y: float, w: float, h: float, label: str, step: str, *, tint: str = IEEE_LIGHT_BLUE) -> None:
    """Shaded column background with step badge."""
    band = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.01,rounding_size=0.10",
        linewidth=1.0,
        edgecolor=IEEE_BLUE,
        facecolor=tint,
        alpha=0.55,
        zorder=0,
    )
    ax.add_patch(band)
    ax.text(
        x + w / 2,
        y + h - 0.18,
        label,
        ha="center",
        va="center",
        fontsize=8.5,
        fontweight="bold",
        color=IEEE_BLUE,
        zorder=2,
    )
    badge = FancyBboxPatch(
        (x + 0.10, y + h - 0.36),
        0.24,
        0.24,
        boxstyle="circle,pad=0.02",
        linewidth=0.0,
        facecolor=IEEE_BLUE,
        zorder=2,
    )
    ax.add_patch(badge)
    ax.text(x + 0.22, y + h - 0.24, step, ha="center", va="center", fontsize=7.5, fontweight="bold", color="white", zorder=3)


def _arrow(ax, start: tuple[float, float], end: tuple[float, float], *, color: str = IEEE_GRAY, lw: float = ARROW_LW) -> None:
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle=ARROW_STYLE,
            mutation_scale=ARROW_MUTATION,
            color=color,
            linewidth=lw,
            shrinkA=2,
            shrinkB=2,
            zorder=4,
        )
    )


def _arrow_path(
    ax,
    points: list[tuple[float, float]],
    *,
    color: str = IEEE_GRAY,
    lw: float = ARROW_LW,
) -> None:
    for i in range(len(points) - 2):
        x0, y0 = points[i]
        x1, y1 = points[i + 1]
        ax.plot([x0, x1], [y0, y1], color=color, linewidth=lw, solid_capstyle="round", zorder=3)
    _arrow(ax, points[-2], points[-1], color=color, lw=lw)


def _draw_accent_box(
    ax,
    x: float,
    y: float,
    w: float,
    h: float,
    label: str,
    sub: str | None = None,
    *,
    accent: str = IEEE_BLUE,
    face: str = "#ffffff",
    lw: float = BOX_LW,
    fontsize: float = SUBTITLE_SIZE,
    bold: bool = False,
    bar_w: float = 0.07,
) -> None:
    """Box with a coloured left accent bar for clearer hierarchy."""
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.10",
        linewidth=lw,
        edgecolor=accent,
        facecolor=face,
        zorder=2,
    )
    ax.add_patch(patch)
    ax.add_patch(
        FancyBboxPatch(
            (x + 0.02, y + 0.06),
            bar_w,
            h - 0.12,
            boxstyle="round,pad=0.0,rounding_size=0.04",
            linewidth=0.0,
            facecolor=accent,
            zorder=3,
        )
    )
    weight = "bold" if bold else "normal"
    tx = x + w / 2 + bar_w * 0.18
    if sub:
        ax.text(tx, y + h * 0.57, label, ha="center", va="center", fontsize=fontsize, fontweight=weight, color=IEEE_DARK)
        ax.text(
            tx,
            y + h * 0.32,
            sub,
            ha="center",
            va="center",
            fontsize=fontsize - 1.5,
            style="italic",
            color=IEEE_GRAY,
        )
    else:
        ax.text(tx, y + h / 2, label, ha="center", va="center", fontsize=fontsize, fontweight=weight, color=IEEE_DARK)


def _route_arrow(
    ax,
    points: list[tuple[float, float]],
    *,
    color: str = IEEE_GRAY,
    lw: float = ARROW_LW,
    style: str = ARROW_STYLE,
) -> None:
    for i in range(len(points) - 2):
        x0, y0 = points[i]
        x1, y1 = points[i + 1]
        ax.plot([x0, x1], [y0, y1], color=color, linewidth=lw, solid_capstyle="round", zorder=1)
    ax.add_patch(
        FancyArrowPatch(
            points[-2],
            points[-1],
            arrowstyle=style,
            mutation_scale=ARROW_MUTATION,
            color=color,
            linewidth=lw,
            shrinkA=0,
            shrinkB=2,
            zorder=1,
        )
    )


def _draw_box(
    ax,
    x: float,
    y: float,
    w: float,
    h: float,
    label: str,
    sub: str | None = None,
    *,
    face: str = IEEE_LIGHT_BLUE,
    edge: str = IEEE_BLUE,
    lw: float = 1.0,
    fontsize: float = 9.0,
    bold: bool = False,
) -> None:
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.10",
        linewidth=lw,
        edgecolor=edge,
        facecolor=face,
        zorder=2,
    )
    ax.add_patch(patch)
    weight = "bold" if bold else "normal"
    if sub:
        ax.text(x + w / 2, y + h * 0.58, label, ha="center", va="center", fontsize=fontsize, fontweight=weight)
        ax.text(
            x + w / 2,
            y + h * 0.28,
            sub,
            ha="center",
            va="center",
            fontsize=fontsize - 1.5,
            style="italic",
            color=IEEE_GRAY,
        )
    else:
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fontsize, fontweight=weight)


def figure_01_framework() -> None:
    """Vertical pipeline layout — avoids column-width overlap when scaled to \\linewidth."""
    apply_rc()
    fig_w, fig_h = 7.2, 7.0
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.set_xlim(0, fig_w)
    ax.set_ylim(0, fig_h)
    ax.axis("off")

    cx = fig_w / 2
    ax.text(cx, 6.72, "PF-STGT Multi-Task Forecasting Framework", ha="center", fontsize=12.5, fontweight="bold", color=IEEE_DARK)
    ax.plot([0.55, fig_w - 0.55], [6.55, 6.55], color=IEEE_MUTED, linewidth=0.7, alpha=0.5, zorder=0)

    bw, bh, gap = 2.05, 0.58, 0.24
    y = 5.72
    row_w = 3 * bw + 2 * gap
    x0 = cx - row_w / 2
    xs = [x0, x0 + bw + gap, x0 + 2 * (bw + gap)]
    input_labels = [
        ("Node features", "$T{=}7$, $N{=}9$, $F_n{=}9$"),
        ("Global context", "$T{=}7$, $F_g{=}17$"),
        ("Corr. graph $\\mathbf{A}$", "$\\tau{=}0.65$"),
    ]
    for x, (title, sub) in zip(xs, input_labels):
        _draw_accent_box(ax, x, y, bw, bh, title, sub, accent=IEEE_ACCENT, fontsize=8.0, bar_w=0.05)

    y_emb = 4.55
    emb_w = 4.55
    _draw_accent_box(
        ax,
        cx - emb_w / 2,
        y_emb,
        emb_w,
        0.68,
        "Embedding + positional encoding",
        "node and global tensors",
        accent=IEEE_BLUE,
        lw=1.2,
        bold=True,
        fontsize=8.5,
        bar_w=0.05,
    )

    y_br = 3.18
    tw = 2.35
    _draw_accent_box(ax, cx - tw - 0.28, y_br, tw, 0.62, "Graph transformer", "spatial attention", accent=IEEE_BLUE, fontsize=8.0, bar_w=0.05)
    _draw_accent_box(ax, cx + 0.28, y_br, tw, 0.62, "Temporal transformer", "lag attention", accent=IEEE_BLUE, fontsize=8.0, bar_w=0.05)

    y_fus = 2.05
    fus_w = 3.55
    _draw_accent_box(
        ax,
        cx - fus_w / 2,
        y_fus,
        fus_w,
        0.62,
        "Gated parallel fusion",
        "spatial + temporal branches",
        accent=IEEE_GREEN,
        face="#f0fff4",
        lw=1.4,
        bold=True,
        fontsize=8.5,
        bar_w=0.05,
    )

    y_out = 0.72
    ow = 2.55
    _draw_accent_box(
        ax,
        cx - ow - 0.22,
        y_out,
        ow,
        0.68,
        "Demand head",
        "9 regional MW",
        accent=IEEE_GREEN,
        face="#f0fff4",
        bold=True,
        fontsize=8.5,
        bar_w=0.05,
    )
    _draw_accent_box(
        ax,
        cx + 0.22,
        y_out,
        ow,
        0.68,
        "Stress head",
        "graph-level OSI",
        accent=IEEE_GREEN,
        face="#f0fff4",
        bold=True,
        fontsize=8.5,
        bar_w=0.05,
    )

    merge_y = 5.15
    for i, x in enumerate(xs):
        if i == 2:
            continue
        _arrow(ax, (x + bw / 2, y), (cx, merge_y), color=IEEE_ACCENT, lw=ARROW_LW)
    _arrow(ax, (cx, merge_y), (cx, y_emb + 0.68), color=IEEE_ACCENT, lw=ARROW_LW)

    _arrow(ax, (cx - 0.55, y_emb), (cx - tw / 2 - 0.28, y_br + 0.62), color=IEEE_BLUE, lw=ARROW_LW)
    _arrow(ax, (cx + 0.55, y_emb), (cx + tw / 2 + 0.28, y_br + 0.62), color=IEEE_BLUE, lw=ARROW_LW)
    _arrow_path(
        ax,
        [
            (xs[2] + bw / 2, y),
            (xs[2] + bw / 2, y_br + 1.05),
            (cx - tw / 2 - 0.28, y_br + 1.05),
            (cx - tw / 2 - 0.28, y_br + 0.62),
        ],
        color=IEEE_ACCENT,
        lw=ARROW_LW,
    )

    _arrow(ax, (cx - tw / 2 - 0.28, y_br), (cx - 0.55, y_fus + 0.62), color=IEEE_GREEN, lw=ARROW_LW_EMPHASIS)
    _arrow(ax, (cx + tw / 2 + 0.28, y_br), (cx + 0.55, y_fus + 0.62), color=IEEE_GREEN, lw=ARROW_LW_EMPHASIS)

    _arrow(ax, (cx - 0.55, y_fus), (cx - ow / 2 - 0.22, y_out + 0.68), color=IEEE_GREEN, lw=ARROW_LW_EMPHASIS)
    _arrow(ax, (cx + 0.55, y_fus), (cx + ow / 2 + 0.22, y_out + 0.68), color=IEEE_GREEN, lw=ARROW_LW_EMPHASIS)

    ax.text(
        cx,
        0.18,
        "Frozen S2: correlation-only graph; seven-day lookback; dual-task decoding",
        ha="center",
        fontsize=7.8,
        style="italic",
        color=IEEE_GRAY,
    )

    export_triple(fig, FIG / "figure_01_framework")
    plt.close(fig)


def figure_02_s2_architecture() -> None:
    """Three-tier S2 diagram with explicit gutters — no box overlap."""
    apply_rc()
    fig_w, fig_h = 10.5, 5.35
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.set_xlim(0, fig_w)
    ax.set_ylim(0, fig_h)
    ax.axis("off")

    cx = fig_w / 2
    ax.text(cx, 5.05, "Frozen S2 Architecture — Correlation-Only PF-STGT", ha="center", fontsize=12.0, fontweight="bold", color=IEEE_DARK)

    # Tier 1 — model selection
    sel_y, sel_h = 3.42, 1.22
    ax.add_patch(
        FancyBboxPatch(
            (0.35, sel_y),
            fig_w - 0.70,
            sel_h,
            boxstyle="round,pad=0.02,rounding_size=0.10",
            linewidth=BOX_LW,
            edgecolor=IEEE_BLUE,
            facecolor=IEEE_LIGHT_BLUE,
            alpha=0.30,
            zorder=0,
        )
    )
    ax.text(0.55, sel_y + sel_h - 0.12, "Model selection", ha="left", fontsize=8.5, fontweight="bold", color=IEEE_GRAY)

    s1_w, s1_h = 2.05, 0.58
    s1_x = 0.65
    s1_y = sel_y + 0.34
    ax.add_patch(
        FancyBboxPatch(
            (s1_x, s1_y),
            s1_w,
            s1_h,
            boxstyle="round,pad=0.02,rounding_size=0.08",
            linewidth=0.9,
            edgecolor=IEEE_RED,
            facecolor="#fafafa",
            linestyle="dashed",
            alpha=0.70,
            zorder=1,
        )
    )
    ax.text(s1_x + s1_w / 2, s1_y + s1_h * 0.68, "S1 (superseded)", ha="center", fontsize=7.2, color=IEEE_GRAY, style="italic")
    ax.text(s1_x + s1_w / 2, s1_y + s1_h * 0.28, "Hybrid geo + corr.", ha="center", fontsize=6.8, color=IEEE_MUTED)

    s2_x, s2_w = 3.15, 6.85
    s2_y = sel_y + 0.26
    s2_h = 0.86
    ax.add_patch(
        FancyBboxPatch(
            (s2_x - 0.06, s2_y - 0.06),
            s2_w + 0.12,
            s2_h + 0.12,
            boxstyle="round,pad=0.02,rounding_size=0.10",
            linewidth=0.0,
            facecolor=IEEE_GREEN,
            alpha=0.10,
            zorder=1,
        )
    )
    ax.add_patch(
        FancyBboxPatch(
            (s2_x, s2_y),
            s2_w,
            s2_h,
            boxstyle="round,pad=0.02,rounding_size=0.10",
            linewidth=BOX_LW_HERO,
            edgecolor=IEEE_GREEN,
            facecolor=IEEE_LIGHT_GREEN,
            zorder=2,
        )
    )
    ax.text(s2_x + s2_w / 2, s2_y + s2_h * 0.72, "S2 — Final model (A6)", ha="center", fontsize=10.0, fontweight="bold", color=IEEE_DARK)
    ax.text(
        s2_x + s2_w / 2,
        s2_y + s2_h * 0.30,
        "Correlation graph only  |  $\\tau{=}0.65$  |  749,058 params",
        ha="center",
        fontsize=7.8,
        color=IEEE_GRAY,
    )

    gain_x = s1_x + s1_w + 0.12
    _arrow(ax, (s1_x + s1_w, s1_y + s1_h / 2), (s2_x, s2_y + s2_h / 2), color=IEEE_GREEN, lw=ARROW_LW_EMPHASIS)
    ax.add_patch(
        FancyBboxPatch(
            (gain_x, s1_y + s1_h + 0.06),
            0.82,
            0.26,
            boxstyle="round,pad=0.02,rounding_size=0.05",
            linewidth=0.8,
            edgecolor=IEEE_GREEN,
            facecolor="white",
            zorder=3,
        )
    )
    ax.text(gain_x + 0.41, s1_y + s1_h + 0.19, "$-$4.66 MW", ha="center", fontsize=7.5, fontweight="bold", color=IEEE_GREEN)

    # Tier 2 — encoder trunk
    trunk_y, trunk_h = 1.95, 1.25
    ax.add_patch(
        FancyBboxPatch(
            (0.35, trunk_y),
            fig_w - 0.70,
            trunk_h,
            boxstyle="round,pad=0.02,rounding_size=0.10",
            linewidth=BOX_LW,
            edgecolor=IEEE_BLUE,
            facecolor="#ffffff",
            zorder=0,
        )
    )
    ax.text(cx, trunk_y + trunk_h - 0.14, "Shared PF-STGT encoder trunk", ha="center", fontsize=8.8, fontweight="bold", color=IEEE_DARK)

    box_y = trunk_y + 0.22
    box_h = 0.58
    specs = [
        (0.55, 2.15, "Node + global", "embedding"),
        (2.95, 2.05, "Graph transformer", "spatial attn."),
        (5.25, 2.05, "Temporal transformer", "lag attn."),
        (7.55, 2.10, "Gated fusion", None),
    ]
    for i, (x, w, title, sub) in enumerate(specs):
        face = IEEE_LIGHT_GREEN if i == 3 else IEEE_LIGHT_BLUE
        edge = IEEE_GREEN if i == 3 else IEEE_BLUE
        bold = i == 3
        _draw_box(ax, x, box_y, w, box_h, title, sub, face=face, edge=edge, fontsize=7.8, bold=bold, lw=BOX_LW)
        if i < len(specs) - 1:
            x_end = x + w
            x_next = specs[i + 1][0]
            col = IEEE_GREEN if i == 2 else IEEE_GRAY
            lw = ARROW_LW_EMPHASIS if i == 2 else ARROW_LW
            _arrow(ax, (x_end, box_y + box_h / 2), (x_next, box_y + box_h / 2), color=col, lw=lw)

    _arrow(ax, (cx, sel_y), (cx, trunk_y + trunk_h), color=IEEE_GRAY, lw=ARROW_LW)

    # Tier 3 — objective + metrics
    bot_y, bot_h = 0.30, 0.82
    _draw_box(ax, 0.55, bot_y, 4.35, bot_h, "Multi-task objective", "$\\mathcal{L} = \\mathrm{Huber}(D)/100 + 20 \\cdot \\mathrm{MSE}(\\mathrm{OSI})$", fontsize=7.8, lw=BOX_LW)
    _draw_box(
        ax,
        5.35,
        bot_y,
        4.55,
        bot_h,
        "Held-out test performance",
        "Demand MAE: 88.65 MW  |  Stress $R^2$: 0.745",
        face=IEEE_LIGHT_GREEN,
        edge=IEEE_GREEN,
        lw=BOX_LW_HERO,
        fontsize=7.8,
        bold=True,
    )

    _arrow(ax, (cx, trunk_y), (2.72, bot_y + bot_h), color=IEEE_GRAY, lw=ARROW_LW)
    _arrow(ax, (cx, trunk_y), (7.62, bot_y + bot_h), color=IEEE_GREEN, lw=ARROW_LW_EMPHASIS)

    export_triple(fig, FIG / "figure_02_s2_architecture")
    plt.close(fig)


def figure_03_training_curves() -> None:
    from PIL import Image

    apply_rc()
    train = Image.open(EXP01_TRAIN)
    val = Image.open(EXP01_VAL)
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 3.4))
    for ax, img, title in zip(
        axes,
        [train, val],
        ["(a) Training loss (Exp01 W20 reference)", "(b) Validation loss (Exp01 W20 reference)"],
    ):
        ax.imshow(img)
        ax.set_title(title, fontsize=SUBTITLE_SIZE, fontweight="bold", loc="left")
        ax.axis("off")
        for spine in ax.spines.values():
            spine.set_edgecolor(IEEE_BLUE)
            spine.set_linewidth(BOX_LW)
    fig.tight_layout()
    fig.savefig(FIG / "figure_03_training_curves.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def figure_04_benchmark_comparison() -> None:
    apply_rc()
    rows = _read_csv(EXP02)
    order = ["B02", "B03", "B07", "S2", "B06"]
    labels_map = {
        "B02": "Random Forest",
        "B03": "XGBoost",
        "B07": "PF-STGT (S1)",
        "S2": "PF-STGT (S2) [final]",
        "B06": "T-GCN",
    }
    by_id = {r["benchmark_id"]: r for r in rows}
    labels = [labels_map[bid] for bid in order]
    maes = [
        88.64871215820312 if bid == "S2" else float(by_id[bid]["demand_mae"])
        for bid in order
    ]
    colors = [IEEE_GREEN if "S2" in lb else IEEE_ACCENT for lb in labels]

    fig, ax = plt.subplots(figsize=(8.8, 4.4))
    bars = ax.barh(labels, maes, color=colors, edgecolor=IEEE_DARK, linewidth=BAR_EDGE_LW, height=0.62)
    ax.set_xlabel("Test demand MAE (MW)", fontsize=LABEL_SIZE)
    ax.set_title("Benchmark comparison — demand forecasting (test set)", fontweight="bold", fontsize=TITLE_SIZE)
    ax.invert_yaxis()
    style_bar_axes(ax, grid_axis="x")
    for bar, mae in zip(bars, maes):
        ax.text(mae + 2, bar.get_y() + bar.get_height() / 2, f"{mae:.1f}", va="center", fontsize=TICK_SIZE)
    ax.set_xlim(0, max(maes) * 1.15)
    export_triple(fig, FIG / "figure_04_benchmark_comparison")
    plt.close(fig)


def figure_05_ablation_comparison() -> None:
    apply_rc()
    rows = _read_csv(EXP03)
    order = ["A4", "A6", "A3", "A1", "A2", "A5"]
    name_map = {
        "A1": "A1 PF-STGT (S1 ref)",
        "A2": "A2 No Graph",
        "A3": "A3 No Transformer",
        "A4": "A4 Single-Task",
        "A5": "A5 Geo Graph Only",
        "A6": "A6 Corr Graph (S2) [final]",
    }
    by_id = {r["ablation_id"]: r for r in rows}
    labels = [name_map[i] for i in order]
    maes = [float(by_id[i]["demand_mae"]) for i in order]
    colors = []
    hatches = []
    for i in order:
        if i == "A6":
            colors.append(IEEE_GREEN)
            hatches.append("")
        elif i == "A4":
            colors.append(IEEE_LIGHT_BLUE)
            hatches.append("///")
        else:
            colors.append(IEEE_MUTED)
            hatches.append("")

    fig, ax = plt.subplots(figsize=(8.8, 4.6))
    bars = ax.barh(labels, maes, color=colors, edgecolor=IEEE_DARK, linewidth=BAR_EDGE_LW, height=0.62)
    for bar, hatch in zip(bars, hatches):
        bar.set_hatch(hatch)
    ax.set_xlabel("Test demand MAE (MW)", fontsize=LABEL_SIZE)
    ax.set_title("Ablation study — demand MAE (test set)", fontweight="bold", fontsize=TITLE_SIZE)
    ax.invert_yaxis()
    style_bar_axes(ax, grid_axis="x")
    for bar, mae in zip(bars, maes):
        ax.text(mae + 1.5, bar.get_y() + bar.get_height() / 2, f"{mae:.1f}", va="center", fontsize=TICK_SIZE)
    export_triple(fig, FIG / "figure_05_ablation_comparison")
    plt.close(fig)


def copy_explainability_figures() -> None:
    subprocess.run([sys.executable, str(PKG / "replot_frozen_explainability.py")], check=True)


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
