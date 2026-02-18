# Story 1.3: 封装基础 ADB 交互动作

Status: done

## Story

As a 开发者,
I want 封装模拟点击、长按、滑动的基础原子操作,
so that 引擎可以像真人一样操控手机 App。

## Acceptance Criteria

1. 点击功能可靠：支持物理像素坐标点击。 [x]
2. 滑动功能可靠：支持指定起点、终点和持续时间的滑动。 [x]
3. 长按功能支持：支持在指定位置停留特定耗时的长按。 [x]
4. 集成归一化：支持直接传入归一化坐标执行动作（自动调用 Transformer）。 [x]
5. 异常保护：当设备未连接时调用动作应抛出清晰异常。 [x]

## Tasks / Subtasks

- [x] 实现核心输入处理类 `InputHandler` (AC: 1, 2, 3)
  - [x] 实现 `click` 方法
  - [x] 实现 `swipe` 方法
  - [x] 实现 `long_press` 方法
- [x] 封装归一化动作接口 (AC: 4)
  - [x] 实现 `stealth_click` 等比例坐标操作
- [x] 验证与测试 (AC: 5)
  - [x] 编写 `src/adb/test_input_handler.py` (Mock ADB)

## Dev Notes

- **Implementation:** 放在 `src/adb/input_handler.py`。
- **Command:** 使用 `ppadb` 的 `device.shell("input tap x y")`。

### Project Structure Notes

- **Naming:** 遵循 `snake_case`。
- **Type Hinting:** 严格使用 TypedDict 处理坐标。

### References

- [Source: _bmad-output/architecture.md#Device Communication & ADB]
- [Source: _bmad-output/epics.md#Story 1.3]

## Dev Agent Record

### Agent Model Used

Gemini 2.0 Flash

### Debug Log References

### Completion Notes List
- 已完成 src/adb/input_handler.py 核心类编写。
- 实现了 click, swipe, long_press 原子操作。
- 实现了与 CoordinateTransformer 集成的归一化操作接口。
- 完成单元测试 src/adb/test_input_handler.py 并验证指令生成的正确性。

### File List
- src/adb/input_handler.py
- src/adb/test_input_handler.py
