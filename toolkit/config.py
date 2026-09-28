"""JSON configuration loader with validation."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ToolkitConfig:
    log_window_seconds: int = 60
    log_error_threshold: int = 5
    csv_quality_warning: float = 80.0


def load_config(path: str | Path | None = None) -> ToolkitConfig:
    if path is None:
        return ToolkitConfig()
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    config = ToolkitConfig(**raw)
    if config.log_window_seconds <= 0 or config.log_error_threshold <= 0:
        raise ValueError("日志窗口和错误阈值必须为正整数")
    if not 0 <= config.csv_quality_warning <= 100:
        raise ValueError("CSV 质量告警阈值必须在 0 到 100 之间")
    return config

