"""PyTorch dataset bridging Sprint 01 foundation pipelines."""

from __future__ import annotations

from typing import Any

import numpy as np
import torch
from torch.utils.data import Dataset

from foundation import FoundationCoordinator


class SmartGridTorchDataset(Dataset):
    """Windowed samples from a chronological split."""

    def __init__(self, split: str, coordinator: FoundationCoordinator) -> None:
        self.split = split
        self.coordinator = coordinator
        self.sample_indices = coordinator.data_result.sample_indices[split]
        self.split_frames = coordinator.data_result.store.get_split(split)
        self.adjacency = coordinator.x_graph.adjacency.astype(np.float32)
        self.attention_bias = coordinator.x_graph.attention_bias.astype(np.float32)

    def __len__(self) -> int:
        return len(self.sample_indices)

    def __getitem__(self, index: int) -> dict[str, Any]:
        sample_idx = self.sample_indices[index]
        foundation = self.coordinator.build_sample(self.split, sample_idx.end_idx)
        return {
            "node_features": torch.from_numpy(foundation.x_temporal.node_features).float(),
            "global_features": torch.from_numpy(foundation.x_temporal.global_features).float(),
            "adjacency": torch.from_numpy(self.adjacency).float(),
            "attention_bias": torch.from_numpy(self.attention_bias).float(),
            "demand_target": torch.from_numpy(foundation.targets.y_demand.values).float(),
            "osi_target": torch.tensor([foundation.targets.y_osi.value], dtype=torch.float32),
            "date_end": str(sample_idx.date_end.date()),
        }


def collate_smartgrid_batch(batch: list[dict[str, Any]]) -> dict[str, torch.Tensor]:
    """Stack batch tensors; adjacency is shared across samples."""
    return {
        "node_features": torch.stack([item["node_features"] for item in batch], dim=0),
        "global_features": torch.stack([item["global_features"] for item in batch], dim=0),
        "adjacency": batch[0]["adjacency"],
        "attention_bias": batch[0]["attention_bias"],
        "demand_target": torch.stack([item["demand_target"] for item in batch], dim=0),
        "osi_target": torch.stack([item["osi_target"] for item in batch], dim=0),
    }
