"""CSV data quality profiler using only the Python standard library."""

from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
from collections import Counter
from pathlib import Path
from typing import Any


MISSING = {"", "null", "none", "na", "n/a", "nan"}


def _is_missing(value: str) -> bool:
    return value.strip().lower() in MISSING


def _as_number(value: str) -> float | None:
    try:
        number = float(value)
        return number if math.isfinite(number) else None
    except ValueError:
        return None


def profile_csv(path: str | Path) -> dict[str, Any]:
    """Return a structured quality report for a UTF-8 CSV file."""
    source = Path(path)
    with source.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError("CSV 文件缺少表头")
        rows = list(reader)

    columns: dict[str, Any] = {}
    for name in reader.fieldnames:
        values = [(row.get(name) or "").strip() for row in rows]
        present = [value for value in values if not _is_missing(value)]
        numbers = [_as_number(value) for value in present]
        numeric = [value for value in numbers if value is not None]
        top_values = Counter(present).most_common(3)
        info: dict[str, Any] = {
            "type": "number" if present and len(numeric) == len(present) else "text",
            "missing": len(values) - len(present),
            "unique": len(set(present)),
            "top_values": top_values,
        }
        if numeric:
            ordered = sorted(numeric)
            info["numeric"] = {
                "min": min(numeric),
                "max": max(numeric),
                "mean": round(sum(numeric) / len(numeric), 4),
                "median": statistics.median(ordered),
            }
        columns[name] = info

    duplicate_count = len(rows) - len({tuple(row.get(k, "") for k in reader.fieldnames) for row in rows})
    total_cells = max(1, len(rows) * len(reader.fieldnames))
    missing_cells = sum(item["missing"] for item in columns.values())
    penalty = (missing_cells / total_cells) * 60 + (duplicate_count / max(1, len(rows))) * 40
    return {
        "file": source.name,
        "rows": len(rows),
        "columns_count": len(reader.fieldnames),
        "duplicate_rows": duplicate_count,
        "quality_score": round(max(0, 100 - penalty), 1),
        "columns": columns,
    }


def render(report: dict[str, Any]) -> str:
    lines = [
        f"文件: {report['file']}",
        f"规模: {report['rows']} 行 × {report['columns_count']} 列",
        f"重复行: {report['duplicate_rows']}",
        f"数据质量评分: {report['quality_score']}/100",
        "",
    ]
    for name, info in report["columns"].items():
        lines.append(f"- {name}: {info['type']} | 缺失 {info['missing']} | 唯一值 {info['unique']}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="生成 CSV 数据质量报告")
    parser.add_argument("csv_file", help="CSV 文件路径")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args()
    report = profile_csv(args.csv_file)
    print(json.dumps(report, ensure_ascii=False, indent=2) if args.json else render(report))


if __name__ == "__main__":
    main()

