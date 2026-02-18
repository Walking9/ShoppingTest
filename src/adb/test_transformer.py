import unittest
import sys
from unittest.mock import MagicMock

# Mock loguru
mock_loguru = MagicMock()
sys.modules["loguru"] = mock_loguru

from src.adb.transformer import CoordinateTransformer

class TestCoordinateTransformer(unittest.TestCase):
    def test_normalize_to_pixel_1080p(self):
        # 测试 1080x1920 屏幕
        transformer = CoordinateTransformer(1080, 1920)
        
        # 中心点
        pixel = transformer.normalize_to_pixel(0.5, 0.5)
        self.assertEqual(pixel, {"x": 540, "y": 960})
        
        # 左上角
        pixel = transformer.normalize_to_pixel(0.0, 0.0)
        self.assertEqual(pixel, {"x": 0, "y": 0})
        
        # 右下角
        pixel = transformer.normalize_to_pixel(1.0, 1.0)
        self.assertEqual(pixel, {"x": 1080, "y": 1920})

    def test_pixel_to_normalize(self):
        transformer = CoordinateTransformer(1080, 2400)
        
        # 转换一个特定点
        ratio_x, ratio_y = transformer.pixel_to_normalize(540, 1200)
        self.assertEqual(ratio_x, 0.5)
        self.assertEqual(ratio_y, 0.5)

    def test_from_wm_size_parsing(self):
        wm_output = "Physical size: 1440x3200"
        transformer = CoordinateTransformer.from_wm_size(wm_output)
        
        self.assertEqual(transformer.width, 1440)
        self.assertEqual(transformer.height, 3200)

if __name__ == "__main__":
    unittest.main()
