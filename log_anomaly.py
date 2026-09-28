"""Detect bursts of errors and suspicious sources in structured application logs."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, deque
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


LOG_PATTERN = re.compile(
    r"^(?P<time>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})\s+"
    r"(?P<level>DEBUG|INFO|WARNING|ERROR|CRITICAL)\s+"
    r"(?P<source>\S+)\s+(?P<message>.+)$"
)


def parse_line(line: str) -> dict[str, Any] | None:
    match = LOG_PATTERN.match(line.strip())
    if not match:
        return None
    item = match.groupdict()
    item["time"] = datetime.fromisoformat(item["time"])
    return item


def detect_anomalies(path: str | Path, window_seconds: int = 60, threshold: int = 5) -> dict[str, Any]:
    """Detect error bursts within a sliding time window."""
    events = []
    invalid_lines = 0
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        parsed = parse_line(raw)
        if parsed is None:
            invalid_lines += 1
        else:
            events.append(parsed)
    events.sort(key=lambda item: item["time"])

    recent: deque[dict[str, Any]] = deque()
    bursts: list[dict[str, Any]] = []
    for event in events:
        if event["level"] not in {"ERROR", "CRITICAL"}:
            continue
        cutoff = event["time"] - timedelta(seconds=window_seconds)
        while recent and recent[0]["time"] < cutoff:
            recent.popleft()
        recent.append(event)
        if len(recent) == threshold:
            bursts.append({
                "start": recent[0]["time"].isoformat(),
                "end": recent[-1]["time"].isoformat(),
                "count": len(recent),
                "sources": dict(Counter(item["source"] for item in recent)),
            })

    levels = Counter(item["level"] for item in events)
    sources = Counter(item["source"] for item in events if item["level"] in {"ERROR", "CRITICAL"})
    return {
        "parsed_events": len(events),
        "invalid_lines": invalid_lines,
        "level_counts": dict(levels),
        "top_error_sources": sources.most_common(5),
        "error_bursts": bursts,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="检测应用日志中的异常错误突增")
    parser.add_argument("log_file")
    parser.add_argument("--window", type=int, default=60, help="滑动窗口秒数")
    parser.add_argument("--threshold", type=int, default=5, help="触发异常的错误数量")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = detect_anomalies(args.log_file, args.window, args.threshold)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"解析事件: {result['parsed_events']}，无效行: {result['invalid_lines']}")
        print(f"错误来源 Top 5: {result['top_error_sources']}")
        print(f"发现错误突增: {len(result['error_bursts'])} 处")


if __name__ == "__main__":
    main()

