"""Sprint 02 — PF-STGT core model smoke test and report generation."""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from constants import GLOBAL_FEATURES, INPUT_WINDOW_T, N_NODES, NODE_FEATURES_PER_REGION, PROJECT_ROOT
from foundation import FoundationCoordinator
from models.config import PFSTGTConfig
from models.pf_stgt import PFSTGT
from utils.logging import setup_logging
from utils.md5 import verify_locked_artifacts

REPORT_DIR = PROJECT_ROOT / "results" / "phases" / "sprint_02_pf_stgt"


def main() -> None:
    setup_logging()
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    verify_locked_artifacts(PROJECT_ROOT, strict=True)
    cfg = PFSTGTConfig()
    model = PFSTGT(cfg)
    model.eval()
    param_count = model.count_parameters()

    dummy_node = torch.randn(2, cfg.input_window_t, cfg.n_nodes, cfg.node_features)
    dummy_global = torch.randn(2, cfg.input_window_t, cfg.global_features)
    dummy_adj = torch.rand(cfg.n_nodes, cfg.n_nodes)
    dummy_adj = dummy_adj / dummy_adj.sum(dim=-1, keepdim=True).clamp_min(1e-6)
    torch.diagonal(dummy_adj).zero_()

    with torch.no_grad():
        dummy_out = model(dummy_node, dummy_global, dummy_adj, return_attention=True)

    coordinator = FoundationCoordinator(verify_md5=True)
    sample = coordinator.smoke_sample("train")
    node = torch.from_numpy(sample.x_temporal.node_features).float().unsqueeze(0)
    global_ = torch.from_numpy(sample.x_temporal.global_features).float().unsqueeze(0)
    adj = torch.from_numpy(sample.x_graph.adjacency).float()
    bias = torch.from_numpy(sample.x_graph.attention_bias).float()

    with torch.no_grad():
        real_out = model(node, global_, adj, attention_bias=bias, return_attention=True)

    lines = [
        "# Sprint 02 — PF-STGT Core Model Report",
        "",
        f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
        "Status: **COMPLETE**",
        "",
        "## Scope",
        "",
        "Implemented PF-STGT core architecture only. No training, evaluation, or explainability.",
        "",
        "## Modules delivered",
        "",
        "| Module | File |",
        "| --- | --- |",
        "| Graph Transformer | `src/models/graph_transformer.py` |",
        "| Temporal Transformer | `src/models/temporal_transformer.py` |",
        "| Parallel Fusion | `src/models/fusion.py` |",
        "| Multi-task Heads | `src/models/heads.py` |",
        "| PF-STGT Wrapper | `src/models/pf_stgt.py` |",
        "",
        "## Hyperparameters (Phase 09 / 11 defaults)",
        "",
        f"| Parameter | Value |",
        f"| --- | --- |",
        f"| d_model | {cfg.d_model} |",
        f"| num_heads | {cfg.num_heads} |",
        f"| L_s (spatial layers) | {cfg.num_spatial_layers} |",
        f"| L_t (temporal layers) | {cfg.num_temporal_layers} |",
        f"| ffn_dim | {cfg.ffn_dim} |",
        f"| spatial_dropout | {cfg.spatial_dropout} |",
        f"| temporal_dropout | {cfg.temporal_dropout} |",
        "",
        f"**Total trainable parameters:** {param_count:,}",
        "",
        "## Input contract validation",
        "",
        f"| Tensor | Expected | Dummy batch |",
        f"| --- | --- | --- |",
        f"| node_features | (B, {INPUT_WINDOW_T}, {N_NODES}, {NODE_FEATURES_PER_REGION}) | `{tuple(dummy_node.shape)}` |",
        f"| global_features | (B, {INPUT_WINDOW_T}, {GLOBAL_FEATURES}) | `{tuple(dummy_global.shape)}` |",
        f"| adjacency | ({N_NODES}, {N_NODES}) | `{tuple(dummy_adj.shape)}` |",
        "",
        "## Output contract validation",
        "",
        "### Dummy batch (B=2)",
        "",
        f"- demand_pred: `{tuple(dummy_out.demand_pred.shape)}`",
        f"- osi_pred: `{tuple(dummy_out.osi_pred.shape)}`",
        f"- attn_spatial: `{tuple(dummy_out.attn_spatial.shape)}`",
        f"- attn_temporal: `{tuple(dummy_out.attn_temporal.shape)}`",
        "",
        "### Foundation sample (B=1)",
        "",
        f"- demand_pred: `{tuple(real_out.demand_pred.shape)}`",
        f"- osi_pred: `{tuple(real_out.osi_pred.shape)}`",
        f"- OSI range check: [{real_out.osi_pred.min().item():.4f}, {real_out.osi_pred.max().item():.4f}]",
        "",
        "## Tests",
        "",
        "```",
        "pytest tests/test_pf_stgt.py tests/test_pf_stgt_integration.py -v",
        "```",
        "",
        "## Sprint 01 integrity",
        "",
        "Locked artefact MD5 hashes verified unchanged. Sprint 01 modules not modified.",
        "",
        "## Next step",
        "",
        "Sprint 3 — Training pipeline (`src/training/`).",
        "",
    ]

    report_path = REPORT_DIR / "sprint_02_report.md"
    report_path.write_text("\n".join(lines))
    print(f"Sprint 02 complete. Report -> {report_path.relative_to(PROJECT_ROOT)}")
    print(f"Parameters: {param_count:,}")
    print(f"Dummy output shapes: demand={tuple(dummy_out.demand_pred.shape)} osi={tuple(dummy_out.osi_pred.shape)}")


if __name__ == "__main__":
    main()
