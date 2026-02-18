import unittest
from unittest.mock import MagicMock
import sys

# Mock loguru
mock_loguru = MagicMock()
sys.modules["loguru"] = mock_loguru

from src.adb.input_handler import InputHandler

class TestInputHandler(unittest.TestCase):
    def setUp(self):
        self.mock_device = MagicMock()
        self.mock_transformer = MagicMock()
        self.handler = InputHandler(self.mock_device, self.mock_transformer)

    def test_click_command(self):
        self.handler.click(100, 200)
        self.mock_device.shell.assert_called_with("input tap 100 200")

    def test_swipe_command(self):
        self.handler.swipe(100, 200, 300, 400, 500)
        self.mock_device.shell.assert_called_with("input swipe 100 200 300 400 500")

    def test_click_normalized(self):
        # 模拟转换器返回像素点
        self.mock_transformer.normalize_to_pixel.return_value = {"x": 540, "y": 960}
        
        self.handler.click_normalized(0.5, 0.5)
        
        # 验证转换器被调用
        self.mock_transformer.normalize_to_pixel.assert_called_with(0.5, 0.5)
        # 验证最终执行了点击指令
        self.mock_device.shell.assert_called_with("input tap 540 960")

if __name__ == "__main__":
    unittest.main()
