---
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8]
workflowType: 'architecture'
lastStep: 8
status: 'complete'
completedAt: '2026-02-18'
project_name: 'iMaotai'
user_name: 'Cc'
date: '2026-02-18'
---

# Architecture Decision Document

_This document builds collaboratively through step-by-step discovery. Sections are appended as we work through each architectural decision together._

## Project Context Analysis

### Requirements Overview

**Functional Requirements:**
项目包含 23 条 FR，核心在于构建一个基于离线 OCR 和静态 JSON 的通用自动化框架。架构需支持：1. 插件化的任务执行逻辑；2. 本地视觉处理管线；3. 灵活的防检测配置。

**Non-Functional Requirements:**
关键驱动因素包括：1. 严苛的离线隐私限制；2. 毫秒级的视觉响应速度；3. 长期挂机的自恢复能力。

**Scale & Complexity:**
- **Primary Domain:** Python + ADB + Mobile Security + Computer Vision
- **Complexity Level:** High (由于离线推理优化和生理级行为模拟的要求)
- **Estimated Architectural Components:** 核心引擎、OCR 处理器、防检测模块、JSON 解析器、通知系统。

### Technical Constraints & Dependencies

- **Hardware:** 闲置安卓手机（可能存在 CPU 性能瓶颈）。
- **Protocol:** ADB (USB/TCP)。
- **Dependency:** PaddleOCR-Mobile 或同等轻量化离线模型。

### Cross-Cutting Concerns Identified

- **全局异常处理与自愈：** 针对闲置设备的不稳定因素（电量、弹窗）。
- **坐标归一化：** 解决不同分辨率下的适配问题。
- **隐私性：** 确保数据完全不离开本地。

## Starter Template Evaluation

### Primary Technology Domain

**Developer Tool / Automation Framework** —— 基于 Python + ADB 的视觉驱动自动化。

### Starter Options Considered

- **Option A: Flat Script Layout** —— 适合单文件抢购脚本，但难以扩展至多平台，且逻辑混杂。
- **Option B: Structured Python Automation (Selected)** —— 逻辑、视觉、配置解耦，最契合 PRD 中“高扩展性”和“防检测”的要求。

### Selected Starter: Structured Python Automation Layout

**Rationale for Selection:**
该结构通过分离 ADB 控制、OCR 推理和任务逻辑，确保了系统的模块化。它允许开发者在不修改核心引擎的情况下，仅通过增减 `src/tasks/` 下的 JSON 文件来适配新平台。

**Initialization Command:**

```bash
mkdir -p src/{adb,ocr,engine,tasks,utils} config data/{templates,models} tests logs && touch requirements.txt README.md .gitignore src/main.py
```

## Core Architectural Decisions

### Decision Priority Analysis

**Critical Decisions (Block Implementation):**
- **OCR 引擎选择：** PaddleOCR (v3.0.1+ 移动版)。
- **ADB 通信库：** `pure-python-adb` (PPADB)，以减少进程创建开销。
- **配置驱动：** 基于 JSON 的声明式静态任务流。

**Important Decisions (Shape Architecture):**
- **图像预处理：** OpenCV-Python，用于二值化和 ROI 剪裁。
- **随机化数学库：** `numpy` 和 `scipy` 实现非均匀分布模拟。
- **异常通知：** 支持 Webhook 通道（如 Server 酱）。

### Vision & OCR Architecture

- **Engine:** PaddleOCR (Mobile PP-OCRv3/v4)
- **Version:** `paddleocr>=2.7.0`, `paddlepaddle>=2.5.0`
- **Rationale:** 移动端离线识别的行业标准，平衡了识别率与推理时间。
- **Optimization:** 集成 OpenCV 灰度化预处理，降低背景干扰。

### Device Communication & ADB

- **Library:** `pure-python-adb (ppadb)`
- **Version:** `pure-python-adb>=0.3.0`
- **Rationale:** 直接通过 Socket 通信，比 `subprocess` 更适合高频截图和指令发送。
- **Setup:** 宿主机运行标准的 ADB Server。

### Stealth & Anti-Detection Logic

- **Implementation:** 基于 `scipy` 的贝塞尔曲线插值。
- **Features:** 模拟压力感应 (Pressure)、点击面积 (Size) 及随机轨迹抖动。
- **Configuration:** 在 JSON 任务文件中定义防御等级 (1-4)。

### Data & Configuration

- **Format:** 静态 JSON。
- **Location:** `src/tasks/*.json`。
- **Logic:** 引擎解析 JSON 步进流，执行“识别 -> 校验 -> 操作 -> 反馈”的循环。

## Implementation Patterns & Consistency Rules

### Naming Patterns

- **Python 代码规范：** 严格遵循 PEP-8。函数名、变量名、模块名统一使用 `snake_case`。类名使用 `PascalCase`。
- **任务配置文件 (JSON)：** 所有的键名（Key）统一使用 `snake_case`（例如：`target_text`, `click_offset`, `stealth_level`）。

### Structure Patterns

- **模块自包含测试：** 测试文件与源代码文件同目录放置。
  - 例如：`src/ocr/ocr_engine.py` 对应的测试文件为 `src/ocr/test_ocr_engine.py`。
- **配置与数据分离：** 
  - `config/`: 存放设备全局配置。
  - `src/tasks/`: 存放业务逻辑 JSON。
  - `data/`: 存放 OCR 推理模型及图像模板。

### Format Patterns

- **坐标数据交换：** 统一使用字典格式 `{"x": val, "y": val}`，禁止使用元组或数组。
- **数据一致性：** 涉及复杂状态返回时，优先使用 `TypedDict` 或 `dataclasses`。

### Process Patterns

- **统一重试逻辑：** 在 `src/utils/decorators.py` 中定义全局 `@retry_on_failure` 装饰器。
- **日志一致性：** 统一使用 `logging` 模块，格式为 `[TIMESTAMP] [LEVEL] [MODULE] - MESSAGE`。

### Enforcement Guidelines for AI Agents

**所有 AI Agent 必须遵守：**
1. 在编写新功能前，先检查同级目录下是否存在 `test_*.py`。
2. 严禁在 JSON 配置文件中使用 `camelCase`。
3. 坐标传递必须包含显式的 `"x"` 和 `"y"` 键。

## Project Structure & Boundaries

### Complete Project Directory Structure

```text
iMaotai/
├── README.md                   # 项目概述与启动指南
├── requirements.txt            # Python 依赖清单 (paddleocr, opencv, ppadb, scipy)
├── .gitignore                  # 忽略 logs, venv, data/models
├── config/
│   ├── settings.json           # 全局配置 (Webhook, ADB Serial, Log Level)
│   └── stealth_profiles.json   # 防防御等级参数定义 (L1-L4)
├── data/
│   ├── models/                 # PaddleOCR 离线推理模型 (det, rec, cls)
│   └── templates/              # 预定义的 UI 图像模板 (可选)
├── logs/                       # 运行日志归档
├── src/
│   ├── main.py                 # 程序入口
│   ├── adb/
│   │   ├── __init__.py
│   │   ├── device_manager.py   # ADB 连接与状态管理
│   │   ├── input_handler.py    # 生理级轨迹、压感模拟核心
│   │   └── test_adb.py         # ADB 模块单元测试 (Co-located)
│   ├── ocr/
│   │   ├── __init__.py
│   │   ├── ocr_engine.py       # PaddleOCR 推理包装
│   │   ├── pre_processor.py    # OpenCV 图像增强 (灰度、二值化)
│   │   └── test_ocr.py         # 视觉识别单元测试
│   ├── engine/
│   │   ├── __init__.py
│   │   ├── scheduler.py        # 任务流调度核心
│   │   ├── task_parser.py      # JSON 任务解析器
│   │   ├── overlay.py          # Debug 悬浮窗实现
│   │   └── test_engine.py      # 引擎逻辑单元测试
│   ├── tasks/
│   │   └── imaotai.json        # i茅台特定的抢购步骤描述
│   └── utils/
│       ├── __init__.py
│       ├── decorators.py       # @retry_on_failure 装饰器
│       ├── notifier.py         # Webhook 通知推送 (Server酱)
│       └── test_utils.py       # 工具函数单元测试
└── tests/                      # 集成测试与 E2E 场景
    └── test_imaotai_flow.py    # i茅台全流程模拟测试
```

### Architectural Boundaries

**API Boundaries:**
- **Vision API:** `ocr_engine.recognize_text(image_path) -> Dict[str, List[Dict[str, Any]]]`
- **Device API:** `input_handler.stealth_click(device_id, x, y, pressure, size)`
- **Task API:** `task_parser.load_task(json_path) -> List[TaskStep]`

**Component Boundaries:**
- `engine` 拥有最高调度权，`adb` 与 `ocr` 相互独立，仅通过 `engine` 交换数据。
- `utils` 提供跨模块的无状态功能（日志、重试、通知）。

## Architecture Validation Results

### Coherence Validation ✅

**Decision Compatibility:**
所有技术选型均围绕“Python + 离线视觉”展开。PaddleOCR、OpenCV 和 PPADB 在 Python 生态下集成度极高，无版本冲突。

### Requirements Coverage Validation ✅

**Functional Requirements Coverage:**
PRD 中的 23 条 FR 已全部映射到架构组件。特别是防检测逻辑（FR10-14）已在 `input_handler.py` 中明确了基于 `scipy` 的实现方式。

### Implementation Readiness Validation ✅

**Overall Status:** READY FOR IMPLEMENTATION
**Confidence Level:** HIGH

### Implementation Handoff

**AI Agent 指南：**
- 严格遵守 `snake_case` 命名和字典格式坐标。
- 编写新功能模块时，必须在同级目录创建并维护 `test_*.py`。
- 所有的 ADB 和 OCR 操作必须包裹在 `@retry_on_failure` 装饰器中。

**首个实现优先级：**
执行项目结构初始化命令：
`mkdir -p src/{adb,ocr,engine,tasks,utils} config data/{templates,models} tests logs && touch requirements.txt README.md .gitignore src/main.py`

## Architecture Completion Summary

### Workflow Completion

**Architecture Decision Workflow:** COMPLETED ✅
**Total Steps Completed:** 8
**Date Completed:** 2026-02-18
**Document Location:** _bmad-output/architecture.md

### Implementation Handoff

**For AI Agents:**
This architecture document is your complete guide for implementing iMaotai. Follow all decisions, patterns, and structures exactly as documented.

**First Implementation Priority:**
`mkdir -p src/{adb,ocr,engine,tasks,utils} config data/{templates,models} tests logs && touch requirements.txt README.md .gitignore src/main.py`

---

**Architecture Status:** READY FOR IMPLEMENTATION ✅
