import unittest
from unittest.mock import MagicMock, patch
import sys

# 动态 Mock 所有的重度依赖
mock_np = MagicMock()
sys.modules["numpy"] = mock_np
mock_paddle = MagicMock()
sys.modules["paddleocr"] = mock_paddle
mock_loguru = MagicMock()
sys.modules["loguru"] = mock_loguru

from src.ocr.ocr_engine import OcrEngine

class TestOcrEngine(unittest.TestCase):
    @patch('src.ocr.ocr_engine.PaddleOCR')
    def test_result_parsing(self, mock_ocr_class):
        # 1. 设置模拟的 PaddleOCR 返回格式
        fake_result = [[
            [ [[0, 0], [100, 0], [100, 100], [0, 100]], ("预约", 0.99) ]
        ]]
        mock_instance = mock_ocr_class.return_value
        mock_instance.ocr.return_value = fake_result
        
        # 2. 初始化引擎并执行
        engine = OcrEngine()
        results = engine.recognize(MagicMock())  # 传入 mock 图像
        
        # 3. 验证解析逻辑
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["text"], "预约")
        self.assertEqual(results[0]["confidence"], 0.99)
        self.assertEqual(results[0]["center"], {"x": 50, "y": 50})

if __name__ == "__main__":
    unittest.main()
