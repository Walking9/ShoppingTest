import unittest
from unittest.mock import MagicMock, patch
import sys

# Mock 外部库
mock_np = MagicMock()
sys.modules["numpy"] = mock_np
mock_cv2 = MagicMock()
sys.modules["cv2"] = mock_cv2
mock_loguru = MagicMock()
sys.modules["loguru"] = mock_loguru

from src.ocr.screen_capture import ScreenCapturer

class TestScreenCapturer(unittest.TestCase):
    def setUp(self):
        self.mock_device = MagicMock()
        self.capturer = ScreenCapturer(self.mock_device)

    def test_capture_success(self):
        # 模拟字节流
        raw_bytes = b"fake_png_data"
        self.mock_device.screencap.return_value = raw_bytes
        
        # 模拟 cv2.imdecode 返回一个有效数组
        mock_img = MagicMock()
        mock_img.shape = (1920, 1080, 3)
        mock_cv2.imdecode.return_value = mock_img
        
        # 执行
        captured_img = self.capturer.capture()
        
        # 验证逻辑流
        self.assertIsNotNone(captured_img)
        self.mock_device.screencap.assert_called_once()
        mock_cv2.imdecode.assert_called_once()

    def test_capture_empty_error(self):
        self.mock_device.screencap.return_value = None
        captured_img = self.capturer.capture()
        self.assertIsNone(captured_img)

if __name__ == "__main__":
    unittest.main()
