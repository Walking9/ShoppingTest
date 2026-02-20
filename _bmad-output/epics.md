---
stepsCompleted: [1, 2, 3, 4]
status: 'complete'
completedAt: '2026-02-19'
---

# iMaotai - Epic Breakdown (Pivoted: Fixed-Sequence Mode)

## Overview
本项目已转轨为基于“固定坐标序列”的自动化模拟方案。通过预录制点击路径并配合高精度生理级混淆算法，实现极致的抢购响应速度。

## Requirements Inventory

### Functional Requirements (Updated)
FR1: 系统可以基于预设的定时任务自动启动抢购流程。
FR2: 系统可以通过 ADB 指令模拟点击、长按、滑动等基础交互动作。
FR3: 系统可以根据归一化算法自动适配不同屏幕分辨率的点击坐标。
FR4: 系统可以按序执行 JSON 定义的动作序列。
FR5: 系统可以在抢购结束后自动释放资源并息屏。
FR10: 系统可以在每次点击时引入正态分布的随机坐标偏移。
FR11: 系统可以模拟真实手指的物理压感 (Pressure) 变化。
FR12: 系统可以模拟非均匀采样的随机滑动轨迹（贝塞尔曲线）。
FR13: 系统可以在操作间隙引入符合真人特征的随机时间延迟。
FR15: 开发者可以编写并加载静态 JSON 格式的任务动作序列。
FR21: 系统可以通过 Webhook 渠道回传执行结果。

## Epic List

### Epic 1: 基础控制与环境 (Base Control) [Done]
建立 ADB 连接、坐标归一化转换及基础点击封装。

### Epic 2: 坐标采集助手 (Coord Picker Tool)
开发辅助工具，实时采集手机屏幕点击点的归一化坐标，用于生成 JSON 序列。

### Epic 3: 序列执行引擎 (Sequence Engine)
实现解析 JSON 动作流的核心引擎，支持延迟、重试及基本流程控制。

### Epic 4: 专家级防御增强 (Advanced Stealth)
在固定坐标序列中集成贝塞尔轨迹、压感模拟及非均匀采样，规避风控。

## Epic 2: 坐标采集助手 (Coord Picker Tool)

### Story 2.1: 实时坐标抓取脚本
As a 开发者,
I want 在手机上点击时 Mac 端实时显示坐标,
so that 我能快速采集抢购流程中的所有点击位置。

**Acceptance Criteria:**
- **Given** 手机已连接 ADB
- **When** 在手机屏幕执行点击动作
- **Then** 终端实时打印该点的物理坐标 (x, y) 和 归一化坐标 (x_ratio, y_ratio)
- **And** 支持按 Ctrl+C 停止抓取。
