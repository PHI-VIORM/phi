"""Report serialization and safe HTML rendering."""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any


def write_json(report: dict[str, Any], output: str | Path) -> Path:
    target = Path(output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return target


def write_html(report: dict[str, Any], output: str | Path, title: str = "Analysis Report") -> Path:
    """Write a standalone HTML report with escaped values."""
    target = Path(output)
    target.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for key, value in report.items():
        rendered = json.dumps(value, ensure_ascii=False, indent=2) if isinstance(value, (dict, list)) else str(value)
        rows.append(f"<tr><th>{html.escape(str(key))}</th><td><pre>{html.escape(rendered)}</pre></td></tr>")
    document = f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>{html.escape(title)}</title><style>
body{{font:15px/1.6 system-ui;margin:40px auto;max-width:1000px;color:#1e293b;padding:0 20px}}
h1{{color:#0f2747}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #d9e2ec;padding:12px;text-align:left;vertical-align:top}}th{{width:180px;background:#eff6ff}}pre{{margin:0;white-space:pre-wrap}}
</style></head><body><h1>{html.escape(title)}</h1><table>{''.join(rows)}</table></body></html>"""
    target.write_text(document, encoding="utf-8")
    return target

