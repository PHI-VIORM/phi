"""Aggregate warnings into actionable diagnostics."""

from __future__ import annotations

from typing import Any


def diagnostics(result: dict[str, Any]) -> list[dict[str, str]]:
    kind, report = result.get("kind"), result.get("report", {})
    messages = []
    if kind == "csv" and report.get("duplicate_rows", 0):
        messages.append({"level": "warning", "message": "数据中存在重复行"})
    if kind == "log" and report.get("error_bursts"):
        messages.append({"level": "critical", "message": "检测到错误突增"})
    if kind == "task" and report.get("suggestions"):
        messages.append({"level": "warning", "message": "任务描述仍有缺失项"})
    return messages

