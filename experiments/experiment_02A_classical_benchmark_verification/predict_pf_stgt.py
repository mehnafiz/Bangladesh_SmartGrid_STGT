"""Materialize B07 test predictions from W20 checkpoint (inference only)."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import torch
from torch.utils.data import DataLoader

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from constants import PROJECT_ROOT
from foundation import FoundationCoordinator
from models.pf_stgt import PFSTGT
from training.dataset import SmartGridTorchDataset, collate_smartgrid_batch

OUT = Path(__file__).resolve().parent / "predictions"
CKPT = (
    PROJECT_ROOT
    / "experiments/experiment_01B_multitask_optimization_repair/checkpoints/W20/B07/seed_42/best.pt"
)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    coordinator = FoundationCoordinator(verify_md5=True)
    model = PFSTGT()
    payload = torch.load(CKPT, map_location="cpu", weights_only=False)
    model.load_state_dict(payload["model_state_dict"])
    model.eval()

    preds, targets = [], []
    loader = DataLoader(
        SmartGridTorchDataset("test", coordinator),
        batch_size=32,
        collate_fn=collate_smartgrid_batch,
    )
    with torch.no_grad():
        for batch in loader:
            out = model(
                batch["node_features"],
                batch["global_features"],
                batch["adjacency"],
                attention_bias=batch["attention_bias"],
            )
            preds.append(out.demand_pred.cpu().numpy())
            targets.append(batch["demand_target"].cpu().numpy())

    y_true = np.concatenate(targets)
    y_pred = np.concatenate(preds)
    np.save(OUT / "y_true.npy", y_true)
    np.save(OUT / "B07_pf_stgt_demand.npy", y_pred.astype(np.float32))
    print(f"Saved PF-STGT predictions to {OUT}", flush=True)


if __name__ == "__main__":
    main()
