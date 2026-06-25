"""DataLoader factory for PF-STGT training."""

from __future__ import annotations

from torch.utils.data import DataLoader

from foundation import FoundationCoordinator
from training.config import TrainingConfig
from training.dataset import SmartGridTorchDataset, collate_smartgrid_batch


def build_dataloaders(
    coordinator: FoundationCoordinator,
    config: TrainingConfig,
) -> dict[str, DataLoader]:
    loaders: dict[str, DataLoader] = {}
    for split in ("train", "validation", "test"):
        dataset = SmartGridTorchDataset(split, coordinator)
        loaders[split] = DataLoader(
            dataset,
            batch_size=config.batch_size,
            shuffle=(split == "train"),
            num_workers=config.num_workers,
            collate_fn=collate_smartgrid_batch,
        )
    return loaders
