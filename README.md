# Data & AI Coding Toolkit

面向数据分析与 AI Coding 场景的轻量级 Python 工具集。项目仅使用 Python 标准库，无需安装第三方依赖，适合作为课程实践、数据处理和任务质量检查的基础工具。

## 包含程序

| 程序 | 功能 | 运行方式 |
|---|---|---|
| CSV 数据质量分析器 | 统计缺失值、重复行、数值分布和疑似类型 | `python csv_profiler.py examples/sales.csv` |
| 日志异常检测器 | 从日志中识别错误突增、异常 IP 和高频事件 | `python log_anomaly.py examples/app.log` |
| AI Coding 任务检查器 | 检查任务描述是否具备目标、约束、验收标准和测试要求 | `python task_linter.py examples/task.md` |
| 统一批量分析 CLI | 自动识别 CSV、LOG、Markdown，批量输出 JSON 或 HTML 报告 | `python toolkit_cli.py examples --format html` |

## 特点

- 零依赖，可在 Python 3.10+ 直接运行
- 提供命令行参数和 JSON 输出，便于接入自动化流程
- 对空文件、缺失列、格式错误等情况提供明确提示
- 包含单元测试，覆盖关键逻辑和边界条件
- 支持敏感信息扫描、报告趋势对比与统一健康评分

## 快速开始

```bash
python csv_profiler.py examples/sales.csv
python log_anomaly.py examples/app.log --window 60 --threshold 3
python task_linter.py examples/task.md
python toolkit_cli.py examples --config config.example.json --format html --output report.html
python -m unittest discover -s tests -v
```

## 项目结构

```text
.
├── csv_profiler.py       # CSV 数据画像与质量评分
├── log_anomaly.py        # 日志异常检测
├── task_linter.py        # AI Coding 任务描述检查
├── toolkit/              # 配置、批量调度与报告模块
├── toolkit_cli.py        # 统一命令行入口
├── config.example.json   # 可调整的质量阈值配置
├── examples/             # 可直接运行的示例数据
└── tests/                # 单元测试
```

## 设计说明

三个工具均采用“解析输入 → 结构化分析 → 生成报告”的设计，核心函数与命令行界面分离，便于复用和测试。输出默认适合人类阅读，也可通过 `--json` 生成机器可读结果。

`toolkit.security` 在提交或分享数据前扫描常见密钥模式，仅报告类型和行号，避免在报告中再次泄露秘密；`toolkit.comparison` 用于比较两次分析的数值变化；`toolkit.health` 将不同工具结果归一为统一健康状态。

## License

MIT

