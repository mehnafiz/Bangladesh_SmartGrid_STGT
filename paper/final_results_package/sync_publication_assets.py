#!/usr/bin/env python3
"""Sync publication figures from final_results_package to journal and conference trees."""

from __future__ import annotations

import shutil
from pathlib import Path

PKG = Path(__file__).resolve().parent
SRC = PKG / "figures"
LATEX = PKG.parent / "latex" / "figures"
CONF = PKG.parent / "conference" / "figures"

# Basename -> extensions to copy (PDF preferred in wrappers; PNG for Overleaf heatmap fallback)
ASSETS = {
    "figure_01_framework": (".pdf", ".svg", ".png"),
    "figure_02_s2_architecture": (".pdf", ".svg", ".png"),
    "figure_03_training_curves": (".png",),
    "figure_04_benchmark_comparison": (".pdf", ".svg", ".png"),
    "figure_05_ablation_comparison": (".pdf", ".svg", ".png"),
    "figure_06_dual_shap": (".pdf", ".svg", ".png"),
    "figure_06_shap_summary_stress": (".pdf", ".svg", ".png"),
    "figure_06_shap_summary_demand": (".pdf", ".svg", ".png"),
    "figure_07_node_importance": (".pdf", ".svg", ".png"),
    "figure_08_temporal_attribution": (".pdf", ".svg", ".png"),
    "figure_09_stress_attribution": (".pdf", ".svg", ".png"),
}


def _copy_tree(dest: Path) -> list[str]:
    copied: list[str] = []
    dest.mkdir(parents=True, exist_ok=True)
    for stem, exts in ASSETS.items():
        for ext in exts:
            src_file = SRC / f"{stem}{ext}"
            if src_file.exists():
                dst = dest / f"{stem}{ext}"
                shutil.copy2(src_file, dst)
                copied.append(str(dst.relative_to(PKG.parent.parent)))
    return copied


def main() -> None:
    copied = _copy_tree(LATEX) + _copy_tree(CONF)
    print(f"Synced {len(copied)} assets to latex/ and conference/ figures/")
    for p in sorted(set(copied)):
        print(f"  {p}")


if __name__ == "__main__":
    main()
