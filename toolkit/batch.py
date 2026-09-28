"""Batch orchestration for supported input files."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from csv_profiler import profile_csv
from log_anomaly import detect_anomalies
from task_linter import lint_task

from .config import ToolkitConfig


def analyze_file(path: str | Path, config: ToolkitConfig | None = None) -> dict[str, Any]:
    source = Path(path)
    settings = config or ToolkitConfig()
    suffix = source.suffix.lower()
    if suffix == ".csv":
        report = profile_csv(source)
        report["warning"] = report["quality_score"] < settings.csv_quality_warning
        return {"kind": "csv", "report": report}
    if suffix == ".log":
        return {"kind": "log", "report": detect_anomalies(source, settings.log_window_seconds, settings.log_error_threshold)}
    if suffix in {".md", ".txt"}:
        return {"kind": "task", "report": lint_task(source.read_text(encoding="utf-8"))}
    raise ValueError(f"不支持的文件类型: {suffix or '(无扩展名)'}")


def analyze_directory(path: str | Path, config: ToolkitConfig | None = None) -> dict[str, Any]:
    root = Path(path)
    if not root.is_dir():
        raise ValueError("批量分析路径必须是目录")
    items = []
    errors = []
    for source in sorted(p for p in root.iterdir() if p.is_file()):
        try:
            result = analyze_file(source, config)
            items.append({"file": source.name, **result})
        except ValueError as exc:
            errors.append({"file": source.name, "error": str(exc)})
    return {"directory": str(root), "analyzed": len(items), "skipped": len(errors), "items": items, "errors": errors}

