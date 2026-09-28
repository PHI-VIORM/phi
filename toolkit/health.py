"""Create a normalized health summary from toolkit reports."""

from __future__ import annotations

from typing import Any


def summarize(result: dict[str, Any]) -> dict[str, Any]:
    kind = result.get("kind")
    report = result.get("report", {})
    if kind == "csv":
        score = float(report.get("quality_score", 0))
        issues = int(report.get("duplicate_rows", 0)) + sum(c.get("missing", 0) for c in report.get("columns", {}).values())
    elif kind == "task":
        score = float(report.get("score", 0))
        issues = len(report.get("suggestions", []))
    elif kind == "log":
        issues = len(report.get("error_bursts", [])) + int(report.get("invalid_lines", 0))
        score = max(0.0, 100.0 - issues * 10)
    else:
        raise ValueError(f"未知报告类型: {kind}")
    return {"kind": kind, "score": round(score, 1), "issues": issues, "status": "healthy" if score >= 80 else "attention"}

