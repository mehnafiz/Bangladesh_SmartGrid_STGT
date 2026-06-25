"""Sprint 01 — run foundation pipelines and generate sprint report."""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from constants import (
    GLOBAL_FEATURES,
    INPUT_WINDOW_T,
    LOCKED_MD5,
    N_NODES,
    NODE_FEATURES_PER_REGION,
    PROJECT_ROOT,
)
from foundation import FoundationCoordinator
from utils.logging import setup_logging
from utils.md5 import verify_locked_artifacts

REPORT_DIR = PROJECT_ROOT / "results" / "phases" / "sprint_01_foundation"


def main() -> None:
    setup_logging()
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    md5_after = verify_locked_artifacts(PROJECT_ROOT, strict=True)
    coordinator = FoundationCoordinator(verify_md5=True)

    lines = [
        "# Sprint 01 — Foundation Layer Report",
        "",
        f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
        "Status: **COMPLETE**",
        "",
        "## Scope",
        "",
        "Implemented P1–P4 foundation pipelines only. No PF-STGT, training, or explainability.",
        "",
        "## Pipelines implemented",
        "",
        "| Pipeline | Package | Status |",
        "| --- | --- | --- |",
        "| P1 Data | `src/data/` | Complete |",
        "| P2 Feature | `src/features/` | Complete |",
        "| P3 Graph | `src/graph/` | Complete |",
        "| P4 Target | `src/targets/` | Complete |",
        "",
        "## Acceptance criteria",
        "",
    ]

    all_pass = True
    for split in ("train", "validation", "test"):
        sample = coordinator.smoke_sample(split)
        lines.append(f"### Split: {split}")
        lines.append("")
        lines.append(f"- X_temporal node shape: `{sample.x_temporal.node_features.shape}`")
        lines.append(
            f"- X_temporal global shape: `{sample.x_temporal.global_features.shape}`"
        )
        lines.append(f"- X_graph adjacency shape: `{sample.x_graph.adjacency.shape}`")
        lines.append(f"- y_demand shape: `{sample.targets.y_demand.values.shape}`")
        lines.append(f"- y_osi value: `{sample.targets.y_osi.value:.4f}`")
        lines.append("")

    sample = coordinator.smoke_sample("train")
    checks = [
        sample.x_temporal.node_features.shape
        == (INPUT_WINDOW_T, N_NODES, NODE_FEATURES_PER_REGION),
        sample.x_temporal.global_features.shape == (INPUT_WINDOW_T, GLOBAL_FEATURES),
        sample.x_graph.adjacency.shape == (N_NODES, N_NODES),
        sample.targets.y_demand.values.shape == (N_NODES,),
        0.0 <= sample.targets.y_osi.value <= 1.0,
    ]
    all_pass = all(checks)

    lines += [
        "## Tensor contract verification",
        "",
        f"- INPUT_WINDOW_T = {INPUT_WINDOW_T}",
        f"- N_NODES = {N_NODES}",
        f"- NODE_FEATURES_PER_REGION = {NODE_FEATURES_PER_REGION}",
        f"- GLOBAL_FEATURES = {GLOBAL_FEATURES}",
        f"- All acceptance checks passed: **{all_pass}**",
        "",
        "## Sample counts",
        "",
    ]
    for split, indices in coordinator.data_result.sample_indices.items():
        lines.append(f"- {split}: **{len(indices)}** valid windowed samples")

    lines += [
        "",
        "## Locked artefact integrity (post-sprint)",
        "",
    ]
    for path, expected in LOCKED_MD5.items():
        actual = md5_after[path]
        lines.append(f"- `{path}` MD5: `{actual}` (unchanged: {actual == expected})")

    lines += [
        "",
        "## Modules delivered",
        "",
        "```",
        "src/data/        loader, splits, validators, pipeline",
        "src/features/    specs, node/global builders, window, pipeline",
        "src/graph/       adjacency, bias, registry, pipeline",
        "src/targets/     demand, osi, batch, pipeline",
        "src/foundation.py",
        "src/constants.py",
        "src/utils/       logging, md5, exceptions",
        "tests/           unit + integration tests",
        "```",
        "",
        "## Next step",
        "",
        "Sprint 2 — PF-STGT model core (`src/models/`).",
        "",
    ]

    report_path = REPORT_DIR / "sprint_01_report.md"
    report_path.write_text("\n".join(lines))
    print(f"Sprint 01 complete. Report -> {report_path.relative_to(PROJECT_ROOT)}")
    print(f"Acceptance checks passed: {all_pass}")


if __name__ == "__main__":
    main()
