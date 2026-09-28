"""Lightweight secret and sensitive-data scanner for text files."""

from __future__ import annotations

import re
from pathlib import Path


PATTERNS = {
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "github_token": re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    "generic_secret": re.compile(r"(?i)\b(?:api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?[^\s'\"]{8,}"),
}


def scan_text(text: str) -> list[dict[str, object]]:
    findings = []
    for line_number, line in enumerate(text.splitlines(), 1):
        for kind, pattern in PATTERNS.items():
            if pattern.search(line):
                findings.append({"kind": kind, "line": line_number})
    return findings


def scan_file(path: str | Path) -> dict[str, object]:
    source = Path(path)
    findings = scan_text(source.read_text(encoding="utf-8", errors="replace"))
    return {"file": source.name, "safe": not findings, "findings": findings}

