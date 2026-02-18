import unittest
from unittest.mock import MagicMock, patch
import sys

# Mock 外部库并定义数值常量以支持加法运算
mock_cv2 = MagicMock()
mock_cv2.COLOR_BGR2GRAY = 6
mock_cv2.THRESH_BINARY = 0
mock_cv2.THRESH_OTSU = 8
sys.modules["cv2"] = mock_cv2

mock_np = MagicMock()
sys.modules["numpy"] = mock_np
mock_loguru = MagicMock()
sys.modules["loguru"] = mock_loguru

from src.ocr.pre_processor import ImageProcessor

class TestImageProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = ImageProcessor()
        self.mock_img = MagicMock()
        self.mock_img.shape = (100, 100, 3)

    def test_to_gray_call(self):
        self.processor.to_gray(self.mock_img)
        mock_cv2.cvtColor.assert_called_with(self.mock_img, mock_cv2.COLOR_BGR2GRAY)

    def test_apply_threshold_call(self):
        # 模拟 cv2.threshold 返回值 (threshold, image)
        mock_cv2.threshold.return_value = (127, MagicMock())
        
        # 传入一个灰度图（模拟）
        gray_mock = MagicMock()
        gray_mock.shape = (100, 100)
        
        self.processor.apply_threshold(gray_mock)
        
        # 验证调用参数，0 + 8 = 8 (THRESH_BINARY + THRESH_OTSU)
        mock_cv2.threshold.assert_called_with(gray_mock, 0, 255, 8)

    def test_pipeline_flow(self):
        # 重置 Mock 调用状态
        mock_cv2.threshold.reset_mock()
        
        # 执行完整流水线（不开启二值化）
        self.processor.process_for_ocr(self.mock_img, use_binary=False)
        
        # 验证基础步骤执行
        mock_cv2.cvtColor.assert_called()
        # 验证二值化未被调用
        mock_cv2.threshold.assert_not_called()

if __name__ == "__main__":
    unittest.main()
