# Story 2.1: 视觉管线基础 - 极速截图与图像读取

Status: done

## Story

As a 开发者,
I want 通过 ADB 快速获取屏幕截图并读取为内存图像对象,
so that 为后续的文字识别提供实时数据源。

## Acceptance Criteria

1. 截图速度优化：采用高效的截图方式，避免频繁的文件 IO。 [x]
2. 格式自动转换：截图数据能直接转换为 OpenCV (NumPy array) 格式。 [x]
3. 异常处理：设备连接中断或截图失败时能抛出捕获异常。 [x]
4. 资源占用：单次截图内存增长应可控，且能被正确回收。 [x]

## Tasks / Subtasks

- [x] 实现截图组件 `ScreenCapturer` (AC: 1, 2)
  - [x] 实现 ADB screencap 数据流读取
  - [x] 集成 OpenCV 转换
- [x] 优化传输效率 (AC: 1)
  - [x] 评估直接通过 Socket 获取字节流的性能
- [x] 验证与测试 (AC: 3, 4)
  - [x] 编写 `src/ocr/test_screen_capture.py` (Mock ADB)

## Dev Notes

- **Implementation:** 放在 `src/ocr/screen_capture.py`。
- **Library:** 使用 `pure-python-adb` 的 `device.screencap()`。

### Project Structure Notes

- **Naming:** 遵循 `snake_case`。
- **Co-location:** 测试文件放在 `src/ocr/`。

### References

- [Source: _bmad-output/architecture.md#Vision & OCR Architecture]
- [Source: _bmad-output/project-context.md#Language-Specific Rules]

## Dev Agent Record

### Agent Model Used

Gemini 2.0 Flash

### Debug Log References

### Completion Notes List
- 已实现 src/ocr/screen_capture.py 核心类。
- 采用 ppadb.screencap() 获取原始字节流，避免了文件落盘的 IO 开销。
- 实现了与 cv2.imdecode 的集成，直接将截图转换为 NumPy 数组。
- 完成了单元测试 src/ocr/test_screen_capture.py 并通过验证。

### File List
- src/ocr/screen_capture.py
- src/ocr/test_screen_capture.py
