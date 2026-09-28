"""Validation helpers for normalized analysis results."""

from __future__ import annotations

from typing import Any


def validate_result(result: dict[str, Any]) -> list[str]:
    errors = []
    kind = result.get("kind")
    if kind not in {"csv", "log", "task"}:
        errors.append("kind 必须是 csv、log 或 task")
    if not isinstance(result.get("report"), dict):
        errors.append("report 必须是对象")
    return errors

