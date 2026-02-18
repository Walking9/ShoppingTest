---
stepsCompleted: [1, 2, 3, 4]
status: 'complete'
completedAt: '2026-02-18'
---

# iMaotai - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for iMaotai, decomposing the requirements from the PRD, UX Design if it exists, and Architecture requirements into implementable stories.

## Requirements Inventory

### Functional Requirements

FR1: 系统可以基于预设的定时任务自动启动抢购流程。
FR2: 系统可以通过 ADB 指令模拟点击、长按、滑动等基础交互动作。
FR3: 系统可以根据归一化算法自动适配不同屏幕分辨率的点击坐标。
FR4: 系统可以识别并处理抢购流程中的标准 UI 状态切换。
FR5: 系统可以在抢购结束后自动释放资源并进入待机或关闭状态。
FR6: 系统可以利用本地离线 OCR 引擎识别屏幕上的文本内容。
FR7: 系统可以对原始截图进行预处理（如灰度、二值化）以提升识别精度。
FR8: 系统可以根据用户设定的“匹配置信度”阈值过滤识别结果。
FR9: 系统可以支持基于文本相对于特定元素的偏移坐标进行操作。
FR10: 系统可以在每次点击时引入正态分布的随机坐标偏移。
FR11: 系统可以模拟真实手指的物理压感 (Pressure) 变化。
FR12: 系统可以模拟非均匀采样的随机滑动轨迹（贝塞尔曲线）。
FR13: 系统可以在操作间隙引入符合真人特征的随机时间延迟。
FR14: 系统可以根据配置等级开启或关闭特定层级的防检测手段。
FR15: 开发者可以编写并加载静态 JSON 格式的任务描述文件。
FR16: 系统可以解析 JSON 文件中的步骤、文本匹配项及重试逻辑。
FR17: 系统可以读取本地全局配置文件，获取 Webhook 地址及设备信息。
FR18: 系统支持通过命令行参数或配置文件定义启动时间。
FR19: 系统可以检测并记录抢购流程中的超时与匹配失败异常。
FR20: 系统可以在连续匹配失败时触发预设的重试步长或中止保护。
FR21: 系统可以通过 Webhook 渠道（如 Server 酱）回传执行结果日志。
FR22: 系统可以在检测到低电量或设备异常时发送远程预警。
FR23: 开发者可以开启悬浮式 Debug Overlay，实时观察 OCR 识别框与执行状态。

### NonFunctional Requirements

NFR1: OCR 识别时效性：单次离线识别耗时需控制在 800ms 以内。
NFR2: 指令执行延迟：ADB 指令下达至物理执行延迟应低于 100ms。
NFR3: 低功耗运行：后台挂机 CPU 占用率应低于 15%。
NFR4: 全离线视觉处理：严禁将截图 or OCR 文本上传至云端。
NFR5: 生理级随机化：点击坐标重复率为 0%。
NFR6: 无人值守自恢复：App 闪退或弹窗需在 60s 内告警。
NFR7: 网络容错：Webhook 推送需支持至少 3 次重试。
NFR8: 逻辑与配置完全解耦：5 分钟内完成 JSON 适配。

### Additional Requirements

- **Starter Template**: 必须使用 `Structured Python Automation` 布局（src/{adb,ocr,engine,tasks,utils}）。
- **Code Style**: 严格遵守 `snake_case` 命名，字典格式坐标 `{"x": val, "y": val}`。
- **Testing**: 强制要求 Co-located tests（测试文件与源代码同目录）。
- **Infrastructure**: 宿主机需运行标准 ADB Server，依赖 `paddleocr>=2.7.0`, `pure-python-adb>=0.3.0`, `opencv-python`, `scipy`。

### FR Coverage Map

FR1: Epic 3 - 定时启动抢购
FR2: Epic 1 - ADB 基础模拟点击
FR3: Epic 1 - 坐标归一化处理
FR4: Epic 3 - 流程状态切换处理
FR5: Epic 3 - 资源回收与关机逻辑
FR6: Epic 2 - OCR 文字内容识别
FR7: Epic 2 - 截图预处理流水线
FR8: Epic 2 - 置信度阈值过滤
FR9: Epic 2 - 相对坐标偏移计算
FR10: Epic 4 - 正态分布坐标随机化
FR11: Epic 4 - 物理压感模拟实现
FR12: Epic 4 - 贝塞尔曲线轨迹生成
FR13: Epic 4 - 真人特征延迟算法
FR14: Epic 4 - 多级防御开关逻辑
FR15: Epic 3 - 静态 JSON 任务加载
FR16: Epic 3 - 任务指令解析引擎
FR17: Epic 1 - 全局配置读取逻辑
FR18: Epic 1 - 命令行参数启动
FR19: Epic 4 - 错误日志持久化记录
FR20: Epic 4 - 容错重试状态机
FR21: Epic 4 - Webhook 推送通知
FR22: Epic 4 - 设备电量与弹窗监控
FR23: Epic 4 - Debug Overlay 视图实现

## Epic List

### Epic 1: 基础自动化与设备控制 (Base Automation & Device Control)
建立 Python 与手机 ADB 的连接，实现跨分辨率的精准坐标归一化点击。
**FRs covered:** FR2, FR3, FR17, FR18

### Epic 2: 本地视觉处理与 OCR 推理 (Local Vision & OCR Pipeline)
集成 PaddleOCR 移动版模型，建立高效、私密的本地文字识别与定位管线。
**FRs covered:** FR6, FR7, FR8, FR9

### Epic 3: 任务流驱动与状态机 (Task Flow & Execution Engine)
解析声明式 JSON 任务配置，驱动业务逻辑的自动化流转与资源调度。
**FRs covered:** FR1, FR4, FR5, FR15, FR16

### Epic 4: 专家级防御体系与闭环监控 (Expert Stealth & Monitoring)
实现深度的生理级行为混淆，并配合 Webhook 和悬浮窗实现无人值守的闭环监控。
**FRs covered:** FR10, FR11, FR12, FR13, FR14, FR19, FR20, FR21, FR22, FR23

## Epic 1: 基础自动化与设备控制 (Base Automation & Device Control)

建立 Python 与手机 ADB 的连接，实现跨分辨率的精准坐标归一化点击。

### Story 1.1: 依赖环境初始化与 ADB 握手

As a 开发者,
I want 初始化项目依赖并实现 ADB 基础连接,
So that 我能通过 Python 代码获取到闲置手机的控制权。

**Acceptance Criteria:**

**Given** 项目已按架构要求初始化目录结构
**When** 安装 requirements.txt 依赖并运行 `src/adb/device_manager.py`
**Then** 系统能正确读取 `config/settings.json` 中的设备序列号并成功建立 Socket 连接
**And** 能够在控制台打印出目标设备的型号和屏幕分辨率

### Story 1.2: 设备状态采集与坐标归一化工具

As a 开发者,
I want 实现一套坐标归一化计算算法,
So that 针对不同手机屏幕编写的 JSON 任务能够通用。

**Acceptance Criteria:**

**Given** 系统已获取当前连接设备的物理分辨率
**When** 传入归一化坐标值（例如比例值）
**Then** 系统能根据当前设备屏幕尺寸，计算并返回正确的物理像素中心点坐标 {"x": val, "y": val}

### Story 1.3: 封装基础 ADB 交互动作

As a 开发者,
I want 封装模拟点击、长按、滑动的基础原子操作,
So that 引擎可以像真人一样操控手机 App。

**Acceptance Criteria:**

**Given** 已建立 ADB 连接
**When** 调用 `src/adb/input_handler.py` 中的 click(x, y) 或 swipe(...)
**Then** 目标设备上能实时执行对应的物理触控动作
**And** 支持通过字典格式 {"x": val, "y": val} 传递坐标数据

### Story 1.4: 基于配置的 CLI 启动器

As a 开发者,
I want 通过命令行参数启动自动化脚本,
So that 我能方便地在终端控制抢购流程的开始和停止。

**Acceptance Criteria:**

**Given** `config/settings.json` 中已填入 Webhook 和设备信息
**When** 在终端运行 `python src/main.py --task imaotai`
**Then** 系统能正确加载配置，唤醒设备连接模块，并准备好进入任务循环

## Epic 2: 本地视觉处理与 OCR 推理 (Local Vision & OCR Pipeline)

集成 PaddleOCR 移动版模型，建立高效、私密的本地文字识别与定位管线。

### Story 2.1: 视觉管线基础 - 极速截图与图像读取

As a 开发者,
I want 通过 ADB 快速获取屏幕截图并读取为内存图像对象,
So that 为后续的文字识别提供实时数据源。

**Acceptance Criteria:**

**Given** 已建立 ADB 连接
**When** 触发截图指令
**Then** 系统能将截图数据直接转换为 OpenCV 的 Mat 对象或 NumPy 数组
**And** 端到端截图耗时满足 NFR2 要求

### Story 2.2: 图像预处理流水线实现

As a 开发者,
I want 实现图像灰度化与二值化等预处理功能,
So that 在复杂背景或低光照环境下提升 OCR 的识别准确率。

**Acceptance Criteria:**

**Given** 一张原始截图图像
**When** 开启预处理开关并应用 OpenCV 滤波
**Then** 输出图像显著增强文字与背景的对比度
**And** 支持在 Debug 模式下预览处理后的图像

### Story 2.3: 集成离线 OCR 引擎并加载模型

As a 开发者,
I want 在本地集成 PaddleOCR 并加载移动端模型,
So that 程序能在无网络环境下进行高效文字推理。

**Acceptance Criteria:**

**Given** data/models/ 目录下已放置 PP-OCRv3 移动版模型文件
**When** 调用 ocr_engine.recognize() 接口
**Then** 推理引擎返回识别出的文字内容及其对应的物理坐标
**And** 识别过程 100% 离线，识别延迟低于 800ms

### Story 2.4: 文本搜索与坐标提取（含置信度过滤）

As a 开发者,
I want 能够根据关键词查找坐标，并按置信度进行过滤,
So that 只有高度确信的目标才会触发点击，减少误操作。

**Acceptance Criteria:**

**Given** 推理结果列表及目标关键词
**When** 设定置信度阈值为 0.8
**Then** 系统返回符合关键词且得分高于 0.8 的中心点坐标 {"x": val, "y": val}
**And** 支持基于特定文本计算相对偏移量

## Epic 3: 任务流驱动与状态机 (Task Flow & Execution Engine)

解析声明式 JSON 任务配置，驱动业务逻辑的自动化流转与资源调度。

### Story 3.1: 静态 JSON 任务解析器

As a 开发者,
I want 实现 JSON 任务文件的读取与校验逻辑,
So that 我能以声明式的方式定义不同平台的抢购流程。

**Acceptance Criteria:**

**Given** 一个符合规范的 JSON 任务文件
**When** 运行 `src/engine/task_parser.py`
**Then** 系统能将 JSON 转换为 Python 对象，并校验关键字段（如 target_text, action_type）是否存在

### Story 3.2: 任务流执行引擎核心实现

As a 开发者,
I want 实现一个基于状态机的任务执行引擎,
So that 程序能自动化地流转抢购步骤并具备局部重试能力。

**Acceptance Criteria:**

**Given** 已加载 i茅台 JSON 配置
**When** 执行引擎启动并进入主循环
**Then** 系统按序完成“截图->OCR->点击->验证”闭环
**And** 支持在识别失败时，按 JSON 定义的 retry_limit 进行局部步骤重试

### Story 3.3: 流程状态切换与业务校验

As a 开发者,
I want 实现步骤间的逻辑校验,
So that 确保上一步点击生效后再执行下一步。

**Acceptance Criteria:**

**Given** 执行完一次点击动作
**When** 进入下一个 Step 之前
**Then** 系统通过 OCR 验证当前屏幕是否出现了预期的校验文案
**And** 若校验失败则根据策略触发回滚或告警

### Story 3.4: 自动关机与资源清理机制

As a 开发者,
I want 在抢购结束后释放资源并退出,
So that 保护闲置手机的硬件寿命。

**Acceptance Criteria:**

**Given** 任务执行完毕（成功或达到重试上限）
**When** 触发退出逻辑
**Then** 程序自动关闭 ADB 连接，清理临时缓存，并按配置执行手机息屏指令

### Story 3.5: 定时任务调度器实现

As a 开发者,
I want 系统能够根据预设时间自动唤醒任务,
So that 我不需要手动启动脚本，实现真正的无人值守。

**Acceptance Criteria:**

**Given** config 中设定了特定的启动时间（如 09:00:00）
**When** 到达预设时刻
**Then** 调度器模块自动拉起执行引擎开始抢购

## Epic 4: 专家级防御体系与闭环监控 (Expert Stealth & Monitoring)

实现深度的生理级行为混淆，并配合 Webhook 和悬浮窗实现无人值守的闭环监控。

### Story 4.1: 生理级随机化算法实现

As a 开发者,
I want 为每次触控引入正态分布的坐标随机化和抖动延迟,
So that 模拟真人操作的不确定性，降低被风控建模的可能性。

**Acceptance Criteria:**

**Given** 任务步长正在执行
**When** 开启随机化算法
**Then** 点击坐标在目标像素周围按正态分布产生偏移，且等待时间包含随机抖动

### Story 4.2: 高级触控轨迹模拟（贝塞尔曲线与压感）

As a 开发者,
I want 模拟非线性的滑动轨迹与动态压力,
So that 绕过 App 针对标准 ADB 指令流的行为特征扫描。

**Acceptance Criteria:**

**Given** 选定 L2 级防御
**When** 执行触控动作
**Then** 系统生成带加速度的贝塞尔曲线轨迹，并传入动态的 pressure 和 size 参数

### Story 4.3: 多级防御切换逻辑

As a 开发者,
I want 实现防御等级 (L1-L4) 的动态切换逻辑,
So that 能够根据目标 App 的风控强度灵活平衡性能与安全性。

**Acceptance Criteria:**

**Given** JSON 配置中设定了特定 stealth_level
**When** 引擎运行时
**Then** 系统根据等级自动启用或禁用对应的防检测算法模块

### Story 4.4: Webhook 结果推送与日志

As a 开发者,
I want 在任务成功、失败或遇到严重错误时收到即时通知,
So that 无需守在闲置手机旁也能掌握最新状态。

**Acceptance Criteria:**

**Given** 触发了 Webhook 事件
**When** 调用通知接口
**Then** 包含执行日志的消息被准时推送到配置好的远程渠道（如 Server 酱）

### Story 4.5: 设备环境自愈与弹窗识别

As a 开发者,
I want 系统能识别并处理干扰抢购的系统弹窗或硬件低电量状态,
So that 提升无人值守时的整体成功率。

**Acceptance Criteria:**

**Given** OCR 识别结果包含已知的干扰关键词
**When** 开启环境监控
**Then** 系统自动触发对应的清除动作，并在 60s 内发送异常预警（NFR6）

### Story 4.6: 开发者 Debug Overlay

As a 开发者,
I want 在手机屏幕上看到实时的状态悬浮窗,
So that 在调试任务脚本时能直观观察 OCR 识别详情。

**Acceptance Criteria:**

**Given** 开启 debug 参数启动脚本
**When** 引擎执行时
**Then** 手机屏幕上出现一个半透明悬浮窗，实时刷新当前步长、置信度及识别边界
