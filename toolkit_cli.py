"""Unified command-line interface for the toolkit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from toolkit.batch import analyze_directory, analyze_file
from toolkit.config import load_config
from toolkit.reporting import write_html, write_json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="data-ai-toolkit", description="数据质量与 AI Coding 任务分析工具")
    parser.add_argument("input", help="待分析文件或目录")
    parser.add_argument("--config", help="JSON 配置文件")
    parser.add_argument("--format", choices=["text", "json", "html"], default="text")
    parser.add_argument("--output", help="报告输出路径")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    source = Path(args.input)
    config = load_config(args.config)
    result = analyze_directory(source, config) if source.is_dir() else analyze_file(source, config)
    if args.format == "text":
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    output = args.output or ("report.json" if args.format == "json" else "report.html")
    target = write_json(result, output) if args.format == "json" else write_html(result, output, "Data & AI Coding Toolkit Report")
    print(f"报告已生成: {target}")


if __name__ == "__main__":
    main()

