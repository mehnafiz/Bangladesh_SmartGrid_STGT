"""Unified IEEE publication design tokens (Phase 20–24)."""

from __future__ import annotations

from matplotlib import colors as mcolors
from matplotlib.colors import LinearSegmentedColormap

PUBLICATION_DPI = 300

IEEE_BLUE = "#2c5282"
IEEE_LIGHT_BLUE = "#ebf8ff"
IEEE_GREEN = "#276749"
IEEE_LIGHT_GREEN = "#f0fff4"
IEEE_RED = "#c53030"
IEEE_LIGHT_RED = "#fff5f5"
IEEE_GRAY = "#4a5568"
IEEE_DARK = "#1a202c"
IEEE_ACCENT = "#3182ce"
IEEE_MUTED = "#718096"

# Phase 24 — global stroke / typography tokens
BOX_LW = 1.2
BOX_LW_HERO = 1.8
ARROW_LW = 1.25
ARROW_LW_EMPHASIS = 1.45
ARROW_STYLE = "-|>"
ARROW_MUTATION = 12
BAR_EDGE_LW = 0.65
TITLE_SIZE = 11.0
SUBTITLE_SIZE = 9.0
LABEL_SIZE = 10.0
TICK_SIZE = 9.0
ANNOT_SIZE = 8.5

PALETTE = {
    "ieeeblue": IEEE_BLUE,
    "ieeelightblue": IEEE_LIGHT_BLUE,
    "ieeegreen": IEEE_GREEN,
    "ieeelightgreen": IEEE_LIGHT_GREEN,
    "ieeered": IEEE_RED,
    "ieeelightred": IEEE_LIGHT_RED,
    "ieeegray": IEEE_GRAY,
    "ieeedark": IEEE_DARK,
    "ieeeaccent": IEEE_ACCENT,
    "ieeemuted": IEEE_MUTED,
}

# Feature-coalition registry (frozen Phase 12) — short labels for figures
COALITION_SHORT: dict[str, str] = {
    "G1": "Regional demand",
    "G2": "Regional supply",
    "G3": "Regional load",
    "G4": "Lags & rolling",
    "G5": "Share & intensity",
    "G6": "Calendar & trend",
    "G7": "Grid aggregates",
    "G8": "Limitation stack",
    "G9": "Weather anomaly",
    "G10": "Nat. generation",
    "G11": "Shedding indicator",
}

COALITION_ORDER = tuple(f"G{i}" for i in range(1, 12))

RC_PARAMS = {
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
    "font.size": 10,
    "axes.titlesize": TITLE_SIZE,
    "axes.labelsize": LABEL_SIZE,
    "xtick.labelsize": TICK_SIZE,
    "ytick.labelsize": TICK_SIZE,
    "savefig.dpi": PUBLICATION_DPI,
    "savefig.bbox": "tight",
    "figure.dpi": PUBLICATION_DPI,
    "axes.edgecolor": IEEE_DARK,
    "axes.labelcolor": IEEE_DARK,
    "text.color": IEEE_DARK,
    "axes.linewidth": 0.8,
}


def apply_rc() -> None:
    import matplotlib.pyplot as plt

    plt.rcParams.update(RC_PARAMS)


def coalition_tick_labels(gids: tuple[str, ...] | list[str] | None = None) -> list[str]:
    """Two-line ticks: coalition ID + short descriptive name."""
    order = list(gids) if gids is not None else list(COALITION_ORDER)
    return [f"{gid}\n({COALITION_SHORT.get(gid, gid)})" for gid in order]


def style_bar_axes(ax, *, grid_axis: str = "x") -> None:
    """Consistent bar-chart axes styling across Figs. 4–6."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(axis="both", labelsize=TICK_SIZE)
    ax.grid(axis=grid_axis, color=IEEE_MUTED, alpha=0.22, linewidth=0.6, linestyle="--")
    ax.set_axisbelow(True)


def heatmap_cmap() -> LinearSegmentedColormap:
    return mcolors.LinearSegmentedColormap.from_list(
        "ieee_heat",
        ["#ffffff", IEEE_LIGHT_BLUE, IEEE_ACCENT, IEEE_BLUE],
    )


def heatmap_cmap_contrast() -> LinearSegmentedColormap:
    """Sequential cmap without a white floor — better cell-level readability."""
    return mcolors.LinearSegmentedColormap.from_list(
        "ieee_heat_contrast",
        ["#c6dbef", "#9ecae1", IEEE_ACCENT, "#2171b5", IEEE_BLUE],
    )


def export_triple(fig, path_stem) -> None:
    """Save PDF, SVG, and PNG from a matplotlib figure."""
    from pathlib import Path

    stem = Path(path_stem)
    fig.savefig(stem.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(stem.with_suffix(".svg"), bbox_inches="tight")
    fig.savefig(stem.with_suffix(".png"), dpi=PUBLICATION_DPI, bbox_inches="tight")
