# Story 1.4: 基于配置的 CLI 启动器

Status: done

## Story

As a 开发者,
I want 通过命令行参数启动自动化脚本,
so that 我能方便地在终端控制抢购流程的开始和停止。

## Acceptance Criteria

1. 命令行参数解析：支持 `--task` 参数指定任务 JSON 和 `--serial` 覆盖配置。 [x]
2. 自动化链条贯通：程序启动后能自动加载配置、连接设备、初始化转换器及输入处理器。 [x]
3. 优雅退出：支持 Ctrl+C 中断，并能正确清理 ADB 连接资源。 [x]
4. 启动验证：成功连接后能显示当前准备就绪的状态摘要。 [x]

## Tasks / Subtasks

- [x] 实现 `src/main.py` 入口逻辑 (AC: 1, 2)
  - [x] 参数解析 (argparse)
  - [x] 流程初始化闭环
- [x] 增强日志与用户反馈 (AC: 4)
  - [x] 打印就绪状态摘要
- [x] 异常处理与资源清理 (AC: 3)
  - [x] 捕获 `KeyboardInterrupt`
- [x] 验证与测试 (AC: 1)
  - [x] 编写 `src/test_main.py` (Mock 流程)

## Dev Notes

- **Implementation:** 放在 `src/main.py`。
- **Logging:** 使用 `loguru` 进行标准输出。

### Project Structure Notes

- **Naming:** 遵循 `snake_case`。
- **Entry point:** `src/main.py` 是唯一启动点。

### References

- [Source: _bmad-output/architecture.md#Requirements to Structure Mapping]
- [Source: _bmad-output/project-context.md#Usage Guidelines]

## Dev Agent Record

### Agent Model Used

Gemini 2.0 Flash

### Debug Log References

### Completion Notes List
- 已完成 src/main.py 核心启动逻辑编写。
- 实现了命令行参数解析，支持任务选择与设备序列号覆盖。
- 贯通了从配置加载到设备连接的完整初始化链路。
- 完成了 src/test_main.py 单元测试并通过验证。

### File List
- src/main.py
- src/test_main.py
