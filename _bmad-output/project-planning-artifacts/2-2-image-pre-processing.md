# Story 2.2: 图像预处理流水线实现

Status: done

## Story

As a 开发者,
I want 实现图像灰度化与二值化等预处理功能,
so that 在复杂背景或低光照环境下提升 OCR 的识别准确率。

## Acceptance Criteria

1. 灰度化转换：支持将 BGR 彩色截图转换为单通道灰度图。 [x]
2. 二值化处理：支持自适应阈值二值化（Otsu 算法），使文字特征更突出。 [x]
3. 图像降噪：集成中值滤波或高斯模糊以消除图像杂点。 [x]
4. 灵活开关：预处理步骤可通过方法参数自由组合（例如：仅灰度，或灰度+二值化）。 [x]
5. 验证工具：支持在预处理后保存中间过程图像用于调试。 [x]

## Tasks / Subtasks

- [x] 实现 `ImageProcessor` 类 (AC: 1, 2, 3)
  - [x] 实现 `to_gray` 转换
  - [x] 实现 `apply_threshold` (Otsu)
  - [x] 实现 `denoise`
- [x] 封装流水线接口 `process_for_ocr` (AC: 4)
- [x] 验证与测试 (AC: 5)
  - [x] 编写 `src/ocr/test_pre_processor.py` (逻辑验证)

## Dev Notes

- **Implementation:** 放在 `src/ocr/pre_processor.py`。
- **Core Library:** 深度使用 `cv2` (OpenCV)。

### Project Structure Notes

- **Naming:** 遵循 `snake_case`。
- **Co-location:** 测试文件放在 `src/ocr/`。

### References

- [Source: _bmad-output/architecture.md#Vision & OCR Architecture]
- [Source: _bmad-output/project-context.md#Vision]

## Dev Agent Record

### Agent Model Used

Gemini 2.0 Flash

### Debug Log References

### Completion Notes List
- 已完成 src/ocr/pre_processor.py 核心类编写。
- 实现了 to_gray, denoise (medianBlur), 和 apply_threshold (Otsu) 原子方法。
- 封装了 process_for_ocr 流水线接口，支持组合式调用。
- 通过了逻辑验证单元测试 src/ocr/test_pre_processor.py。

### File List
- src/ocr/pre_processor.py
- src/ocr/test_pre_processor.py
