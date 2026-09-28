"""Quality linter for AI coding task descriptions."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


RULES = {
    "goal": ("明确目标", [r"目标", r"实现", r"开发", r"修复"]),
    "input_output": ("说明输入与输出", [r"输入", r"输出", r"返回", r"参数"]),
    "constraints": ("列出技术或业务约束", [r"约束", r"不得", r"必须", r"兼容", r"限制"]),
    "acceptance": ("给出验收标准", [r"验收", r"完成标准", r"满足以下", r"预期结果"]),
    "tests": ("要求测试或示例", [r"测试", r"用例", r"示例", r"边界"]),
    "error_handling": ("说明异常处理", [r"异常", r"错误", r"失败", r"无效"]),
}


def lint_task(text: str) -> dict[str, Any]:
    normalized = re.sub(r"\s+", " ", text).strip()
    checks = []
    for key, (label, patterns) in RULES.items():
        passed = any(re.search(pattern, normalized, re.IGNORECASE) for pattern in patterns)
        checks.append({"id": key, "label": label, "passed": passed})
    passed_count = sum(item["passed"] for item in checks)
    score = round(passed_count / len(checks) * 100)
    suggestions = [item["label"] for item in checks if not item["passed"]]
    if len(normalized) < 80:
        score = max(0, score - 10)
        suggestions.append("增加必要背景，使任务描述达到约 80 字以上")
    return {"score": score, "grade": "优秀" if score >= 85 else "合格" if score >= 60 else "需完善", "checks": checks, "suggestions": suggestions}


def main() -> None:
    parser = argparse.ArgumentParser(description="检查 AI Coding 任务描述的完整性")
    parser.add_argument("task_file")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = lint_task(Path(args.task_file).read_text(encoding="utf-8"))
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"任务质量: {result['score']}/100（{result['grade']}）")
        for item in result["checks"]:
            print(f"{'[OK]' if item['passed'] else '[--]'} {item['label']}")
        if result["suggestions"]:
            print("建议补充：" + "；".join(result["suggestions"]))


if __name__ == "__main__":
    main()

