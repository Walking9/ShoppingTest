# Story 1.2: 设备状态采集与坐标归一化工具

Status: done

## Story

As a 开发者,
I want 实现一套坐标归一化计算算法,
so that 针对不同手机屏幕编写的 JSON 任务能够通用。

## Acceptance Criteria

1. 转换算法准确：支持从归一化坐标 (0.0-1.0) 转换为物理像素坐标。 [x]
2. 双向支持：支持物理坐标反向归一化（便于录制任务）。 [x]
3. 容错处理：当传入非法坐标或设备信息丢失时有明确报错。 [x]
4. 单元测试覆盖：包含对不同比例屏幕转换逻辑的数学验证。 [x]

## Tasks / Subtasks

- [x] 实现坐标转换核心类 (AC: 1, 2)
  - [x] 实现 `normalize_to_pixel`
  - [x] 实现 `pixel_to_normalize`
- [x] 集成至设备管理流程 (AC: 1)
  - [x] 让 `DeviceManager` 支持获取实时分辨率并传递给转换器
- [x] 验证与测试 (AC: 4)
  - [x] 编写 `src/adb/test_transformer.py`
  - [x] 验证 16:9 与 20:9 比例下的转换精度

## Dev Notes

- **Logic:** 归一化坐标定义为 (x_ratio, y_ratio)，其中 (0,0) 为左上角，(1,1) 为右下角。
- **Implementation:** 放在 `src/adb/transformer.py`。

### Project Structure Notes

- **Naming:** 遵循 `snake_case`。
- **Consistency:** 坐标返回格式统一为 `{"x": int, "y": int}`。

### References

- [Source: _bmad-output/architecture.md#Cross-Cutting Concerns Identified]
- [Source: _bmad-output/project-context.md#Critical Don't-Miss Rules]

## Dev Agent Record

### Agent Model Used

Gemini 2.0 Flash

### Debug Log References

### Completion Notes List
- 已完成 src/adb/transformer.py 核心类编写。
- 已更新 src/adb/device_manager.py 以支持自动初始化转换器。
- 已完成单元测试 src/adb/test_transformer.py 并通过数学验证。

### File List
- src/adb/transformer.py
- src/adb/device_manager.py
- src/adb/test_transformer.py
