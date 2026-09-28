"""Find duplicate records and their original positions."""

from __future__ import annotations

from collections import defaultdict
from typing import Any


def duplicate_groups(rows: list[dict[str, Any]], keys: list[str]) -> list[dict[str, object]]:
    if not keys:
        raise ValueError("至少需要一个去重字段")
    groups: dict[tuple[Any, ...], list[int]] = defaultdict(list)
    for index, row in enumerate(rows, 1):
        groups[tuple(row.get(key) for key in keys)].append(index)
    return [{"key": list(key), "rows": positions} for key, positions in groups.items() if len(positions) > 1]

