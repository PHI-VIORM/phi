"""Create a reproducible SHA-256 manifest for project files."""

from __future__ import annotations

import hashlib
from pathlib import Path


def build_manifest(root: str | Path) -> list[dict[str, object]]:
    base = Path(root)
    entries = []
    for path in sorted(p for p in base.rglob("*") if p.is_file() and ".git" not in p.parts):
        data = path.read_bytes()
        entries.append({"path": path.relative_to(base).as_posix(), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    return entries

