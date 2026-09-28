import tempfile
import unittest
from pathlib import Path

from csv_profiler import profile_csv
from log_anomaly import detect_anomalies, parse_line
from task_linter import lint_task
from toolkit.batch import analyze_directory, analyze_file
from toolkit.config import load_config
from toolkit.reporting import write_html


class CsvProfilerTests(unittest.TestCase):
    def test_missing_and_duplicate_detection(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "sample.csv"
            path.write_text("id,value\n1,10\n2,\n1,10\n", encoding="utf-8")
            report = profile_csv(path)
        self.assertEqual(report["duplicate_rows"], 1)
        self.assertEqual(report["columns"]["value"]["missing"], 1)
        self.assertEqual(report["columns"]["id"]["type"], "number")


class LogAnomalyTests(unittest.TestCase):
    def test_invalid_line(self):
        self.assertIsNone(parse_line("not a log line"))

    def test_burst_detection(self):
        content = "\n".join([
            "2026-01-01T00:00:00 ERROR api timeout",
            "2026-01-01T00:00:10 ERROR api timeout",
            "2026-01-01T00:00:20 ERROR db unavailable",
        ])
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "app.log"
            path.write_text(content, encoding="utf-8")
            result = detect_anomalies(path, window_seconds=60, threshold=3)
        self.assertEqual(len(result["error_bursts"]), 1)


class TaskLinterTests(unittest.TestCase):
    def test_complete_task_scores_high(self):
        text = "目标是实现导出功能。输入为 JSON，输出 CSV。必须处理异常。验收标准包含字段一致，并提供边界测试用例。"
        result = lint_task(text)
        self.assertGreaterEqual(result["score"], 85)


class IntegratedToolkitTests(unittest.TestCase):
    def test_dispatches_csv_analysis(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "data.csv"
            path.write_text("id,value\n1,10\n", encoding="utf-8")
            result = analyze_file(path)
        self.assertEqual(result["kind"], "csv")

    def test_batch_skips_unsupported_files(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "task.md").write_text("目标 实现 输入 输出 必须 验收 测试 异常" * 10, encoding="utf-8")
            (root / "image.bin").write_bytes(b"x")
            result = analyze_directory(root)
        self.assertEqual(result["analyzed"], 1)
        self.assertEqual(result["skipped"], 1)

    def test_config_validation(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "config.json"
            path.write_text('{"log_window_seconds": 0}', encoding="utf-8")
            with self.assertRaises(ValueError):
                load_config(path)

    def test_html_output_escapes_values(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "report.html"
            write_html({"value": "<script>"}, output)
            content = output.read_text(encoding="utf-8")
        self.assertIn("&lt;script&gt;", content)
        self.assertNotIn("<script>", content)


if __name__ == "__main__":
    unittest.main()

