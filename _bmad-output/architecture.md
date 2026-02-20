---
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8]
workflowType: 'architecture'
status: 'complete'
completedAt: '2026-02-19'
project_name: 'iMaotai'
user_name: 'Cc'
date: '2026-02-19'
---

# Architecture Decision Document (Pivoted: Fixed-Sequence Mode)

## Project Context Analysis (Updated)
本项目已从“视觉驱动”转轨为“坐标序列驱动”。核心挑战从“本地 OCR 性能”转变为“固定路径下的反检测混淆”。

## Core Architectural Decisions

### 1. 执行逻辑：固定坐标映射
- **模式：** 宿主机存储一组 `(x_ratio, y_ratio)` 构成的 JSON 动作序列。
- **优势：** 零识别延迟，100% 确定性。

### 2. 反检测核心：生理级模拟 (Input Stealth)
- **Library:** `scipy`, `numpy`。
- **Mechanism:** 为每个固定点增加 `±3px` 的高斯分布偏移，并生成非均匀采样的滑动轨迹。

### 3. 连接与通信
- **ADB Library:** `pure-python-adb` (PPADB)。
- **Trigger:** 基于 `main.py` 的定时启动。

## Project Structure & Boundaries (Cleaned)

```text
iMaotai/
├── config/
│   ├── settings.json           # 设备信息、Webhook、全局开关
│   └── workflows/              # 存放抢购动作序列
│       └── imaotai_flow.json   # 固定坐标点击序列
├── src/
│   ├── main.py                 # 入口，执行序列循环
│   ├── adb/
│   │   ├── device_manager.py   # 连接管理
│   │   ├── input_handler.py    # 混淆点击、贝塞尔轨迹 (核心)
│   │   └── transformer.py      # 坐标转换
│   └── utils/
│       ├── config_loader.py    # JSON 加载
│       └── notifier.py         # Webhook 通知
└── tools/
    └── coord_picker.py         # [新增] 辅助采集坐标的小工具
```
