"""MD5 verification for locked phase artefacts."""

from __future__ import annotations

import hashlib
from pathlib import Path

from constants import LOCKED_MD5, PROJECT_ROOT
from utils.exceptions import LockedArtifactError


def compute_md5(path: Path) -> str:
    """Compute MD5 hex digest of a file."""
    digest = hashlib.md5()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_locked_artifacts(
    root: Path | None = None,
    *,
    strict: bool = True,
) -> dict[str, str]:
    """
    Verify locked artefact MD5 hashes.

    Returns mapping of relative path → actual MD5.
    Raises LockedArtifactError when strict=True and a hash mismatches.
    """
    base = root or PROJECT_ROOT
    results: dict[str, str] = {}
    errors: list[str] = []

    for rel_path, expected in LOCKED_MD5.items():
        path = base / rel_path
        if not path.exists():
            errors.append(f"Missing locked artefact: {rel_path}")
            continue
        actual = compute_md5(path)
        results[rel_path] = actual
        if actual != expected:
            errors.append(
                f"MD5 mismatch for {rel_path}: expected {expected}, got {actual}"
            )

    if errors and strict:
        raise LockedArtifactError("\n".join(errors))

    return results
