"""Compare two compatible analysis reports."""

from __future__ import annotations

from typing import Any


def compare_numeric(before: dict[str, Any], after: dict[str, Any], fields: list[str]) -> dict[str, Any]:
    changes = {}
    for field in fields:
        old = before.get(field)
        new = after.get(field)
        if isinstance(old, (int, float)) and isinstance(new, (int, float)):
            changes[field] = {"before": old, "after": new, "delta": round(new - old, 4)}
    return {"changed_fields": len(changes), "changes": changes}

