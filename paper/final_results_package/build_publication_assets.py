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


def _draw_minibox(
    ax,
    x: float,
    y: float,
    w: float,
    h: float,
    label: str,
    sub: str | None = None,
    *,
    lw: float = 0.75,
    fontsize: float = 8.2,
) -> None:
    """Uniform white box for academic system diagrams."""
    ax.add_patch(
        FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.015,rounding_size=0.06",
            linewidth=lw, edgecolor=IEEE_DARK, facecolor="#ffffff", zorder=2,
        )
    )
    if sub:
        ax.text(x + w / 2, y + h * 0.60, label, ha="center", va="center",
                fontsize=fontsize, color=IEEE_DARK, zorder=3)
        ax.text(x + w / 2, y + h * 0.30, sub, ha="center", va="center",
                fontsize=fontsize - 1.4, color=IEEE_GRAY, zorder=3)
    else:
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
                fontsize=fontsize, color=IEEE_DARK, zorder=3)


def figure_01_framework() -> None:
    """Minimal horizontal pipeline — uniform boxes, single-tone arrows."""
    apply_rc()
    fig_w, fig_h = 7.15, 2.72
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.set_xlim(0, fig_w)
    ax.set_ylim(0, fig_h)
    ax.axis("off")

    fs, bh = 8.0, 0.46
    mid = lambda y: y + bh / 2
    arr = IEEE_GRAY
    alw = 1.0

    # Column guides (subtle, no tinted bands)
    for x in (2.02, 5.58):
        ax.plot([x, x], [0.22, 2.38], color=IEEE_MUTED, linewidth=0.45,
                linestyle=(0, (4, 3)), alpha=0.55, zorder=0)
    for label, xc in (("Inputs", 1.01), ("Encoding", 3.80), ("Outputs", 6.37)):
        ax.text(xc, 2.48, label, ha="center", va="bottom",
                fontsize=7.5, fontweight="bold", color=IEEE_GRAY, zorder=1)

    # --- Inputs ---
    x_in, bw_in = 0.30, 1.42
    inputs = [
        (1.82, "Node features", "$T{=}7$, $N{=}9$, $F_n{=}9$"),
        (1.18, "Global context", "$T{=}7$, $F_g{=}17$"),
        (0.54, "Corr. graph $\\mathbf{A}$", "$\\tau{=}0.65$"),
    ]
    for y, title, sub in inputs:
        _draw_minibox(ax, x_in, y, bw_in, bh, title, sub, fontsize=fs)

    # --- Encoding ---
    x_enc, bw_enc = 2.18, 3.22
    y_emb = 1.82
    _draw_minibox(ax, x_enc, y_emb, bw_enc, bh,
                  "Embedding + positional encoding", "node and global tensors", fontsize=fs)

    tw = 1.46
    y_tr = 1.02
    gt_x, tt_x = 2.18, 3.94
    _draw_minibox(ax, gt_x, y_tr, tw, bh, "Graph transformer", "spatial attention", fontsize=fs)
    _draw_minibox(ax, tt_x, y_tr, tw, bh, "Temporal transformer", "lag attention", fontsize=fs)

    fus_w, fus_x, y_fus = 2.12, 2.73, 0.30
    _draw_minibox(ax, fus_x, y_fus, fus_w, bh,
                  "Gated parallel fusion", "spatial + temporal branches", fontsize=fs)

    # --- Outputs ---
    x_out, ow = 5.78, 1.18
    _draw_minibox(ax, x_out, 1.62, ow, bh, "Demand head", "9 regional MW", fontsize=fs)
    _draw_minibox(ax, x_out, 0.54, ow, bh, "Stress head", "graph-level OSI", fontsize=fs)

    # --- Arrows (single colour, orthogonal) ---
    bus_x = 1.92
    ax.plot([bus_x, bus_x], [mid(0.54), mid(1.82)], color=arr, linewidth=alw,
            solid_capstyle="round", zorder=1)
    for y_in in (1.82, 1.18, 0.54):
        ax.plot([x_in + bw_in, bus_x], [mid(y_in), mid(y_in)], color=arr, linewidth=alw, zorder=1)

    _route_arrow(ax, [(bus_x, mid(1.82)), (x_enc, mid(y_emb))], color=arr, lw=alw)
    _route_arrow(ax, [(bus_x, mid(0.54)), (bus_x, mid(y_tr)), (gt_x, mid(y_tr))], color=arr, lw=alw)

    emb_cx = x_enc + bw_enc / 2
    _route_arrow(ax, [(emb_cx - 0.52, y_emb), (emb_cx - 0.52, 0.72),
                      (gt_x + tw / 2, 0.72), (gt_x + tw / 2, y_tr + bh)], color=arr, lw=alw)
    _route_arrow(ax, [(emb_cx + 0.52, y_emb), (emb_cx + 0.52, 0.72),
                      (tt_x + tw / 2, 0.72), (tt_x + tw / 2, y_tr + bh)], color=arr, lw=alw)

    _route_arrow(ax, [(gt_x + tw / 2, y_tr), (gt_x + tw / 2, 0.64),
                      (fus_x + fus_w * 0.28, 0.64), (fus_x + fus_w * 0.28, y_fus + bh)], color=arr, lw=alw)
    _route_arrow(ax, [(tt_x + tw / 2, y_tr), (tt_x + tw / 2, 0.64),
                      (fus_x + fus_w * 0.72, 0.64), (fus_x + fus_w * 0.72, y_fus + bh)], color=arr, lw=alw)

    out_bus = 5.52
    fus_rx = fus_x + fus_w
    _route_arrow(ax, [(fus_rx, mid(y_fus)), (out_bus, mid(y_fus)),
                      (out_bus, mid(1.62)), (x_out, mid(1.62))], color=arr, lw=alw)
    _route_arrow(ax, [(fus_rx, mid(y_fus)), (out_bus, mid(y_fus)),
                      (out_bus, mid(0.54)), (x_out, mid(0.54))], color=arr, lw=alw)

    export_triple(fig, FIG / "figure_01_framework")
    plt.close(fig)


def figure_02_s2_architecture() -> None:
    """Minimal three-tier S2 diagram — uniform boxes, single-tone arrows."""
    apply_rc()
    fig_w, fig_h = 7.15, 3.55
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.set_xlim(0, fig_w)
    ax.set_ylim(0, fig_h)
    ax.axis("off")

    fs, bh = 7.8, 0.44
    arr, alw = IEEE_GRAY, 1.0
    mid = lambda y: y + bh / 2

    # Tier separators (dashed guides, no tinted bands)
    for y in (2.38, 1.28):
        ax.plot([0.22, fig_w - 0.22], [y, y], color=IEEE_MUTED, linewidth=0.45,
                linestyle=(0, (4, 3)), alpha=0.55, zorder=0)

    tier_labels = [
        (3.18, "Model selection"),
        (2.08, "Shared PF-STGT encoder trunk"),
        (0.98, "Objective and held-out metrics"),
    ]
    for y, label in tier_labels:
        ax.text(0.28, y, label, ha="left", va="bottom",
                fontsize=7.5, fontweight="bold", color=IEEE_GRAY, zorder=1)

    # --- Tier 1: S1 → S2 ---
    s1_x, s1_w = 0.32, 1.48
    s1_y = 2.72
    ax.add_patch(
        FancyBboxPatch(
            (s1_x, s1_y), s1_w, bh,
            boxstyle="round,pad=0.015,rounding_size=0.06",
            linewidth=0.75, edgecolor=IEEE_MUTED, facecolor="#ffffff",
            linestyle=(0, (3, 2)), zorder=2,
        )
    )
    ax.text(s1_x + s1_w / 2, s1_y + bh * 0.62, "S1 (superseded)", ha="center", va="center",
            fontsize=fs - 0.6, color=IEEE_GRAY, style="italic", zorder=3)
    ax.text(s1_x + s1_w / 2, s1_y + bh * 0.30, "Hybrid geo + corr.", ha="center", va="center",
            fontsize=fs - 1.4, color=IEEE_MUTED, zorder=3)

    s2_x, s2_w = 2.18, 4.65
    s2_y = 2.70
    _draw_minibox(ax, s2_x, s2_y, s2_w, bh + 0.06,
                  "S2 — Final model (A6)",
                  "Correlation graph only  |  $\\tau{=}0.65$  |  749,058 params",
                  fontsize=fs)

    _route_arrow(ax, [(s1_x + s1_w, mid(s1_y)), (s2_x, mid(s2_y))], color=arr, lw=alw)
    ax.text(s1_x + s1_w + 0.22, mid(s1_y) + 0.18, "$-$4.66 MW", ha="center", va="bottom",
            fontsize=7.2, color=IEEE_DARK, zorder=3)

    # --- Tier 2: encoder chain ---
    enc_y = 1.42
    enc_specs = [
        (0.32, 1.38, "Node + global", "embedding"),
        (1.88, 1.38, "Graph transformer", "spatial attn."),
        (3.44, 1.38, "Temporal transformer", "lag attn."),
        (5.00, 1.38, "Gated fusion", None),
    ]
    for i, (x, w, title, sub) in enumerate(enc_specs):
        _draw_minibox(ax, x, enc_y, w, bh, title, sub, fontsize=fs - 0.2)
        if i < len(enc_specs) - 1:
            x_end = x + w
            x_next = enc_specs[i + 1][0]
            _route_arrow(ax, [(x_end, mid(enc_y)), (x_next, mid(enc_y))], color=arr, lw=alw)

    trunk_cx = fig_w / 2
    _route_arrow(ax, [(trunk_cx, s2_y), (trunk_cx, enc_y + bh)], color=arr, lw=alw)

    # --- Tier 3: objective + metrics ---
    bot_y = 0.30
    _draw_minibox(
        ax, 0.32, bot_y, 3.18, bh + 0.10,
        "Multi-task objective",
        "$\\mathcal{L} = \\mathrm{Huber}(D)/100 + 20 \\cdot \\mathrm{MSE}(\\mathrm{OSI})$",
        fontsize=fs - 0.2,
    )
    _draw_minibox(
        ax, 3.65, bot_y, 3.18, bh + 0.10,
        "Held-out test performance",
        "Demand MAE: 88.65 MW  |  Stress $R^2$: 0.745",
        fontsize=fs - 0.2,
    )

    split_y = 0.88
    _route_arrow(ax, [(trunk_cx, enc_y), (trunk_cx, split_y)], color=arr, lw=alw)
    _route_arrow(ax, [(trunk_cx, split_y), (1.91, split_y), (1.91, bot_y + bh + 0.10)], color=arr, lw=alw)
    _route_arrow(ax, [(trunk_cx, split_y), (5.24, split_y), (5.24, bot_y + bh + 0.10)], color=arr, lw=alw)

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
