from typing import Dict, Tuple
from loguru import logger

class CoordinateTransformer:
    """负责物理像素坐标与归一化比例坐标之间的转换。"""

    def __init__(self, screen_width: int, screen_height: int):
        self.width = screen_width
        self.height = screen_height
        logger.info(f"初始化坐标转换器: {self.width}x{self.height}")

    def normalize_to_pixel(self, x_ratio: float, y_ratio: float) -> Dict[str, int]:
        """从归一化比例 (0.0 - 1.0) 转换为物理像素坐标。"""
        pixel_x = int(x_ratio * self.width)
        pixel_y = int(y_ratio * self.height)
        return {"x": pixel_x, "y": pixel_y}

    def pixel_to_normalize(self, pixel_x: int, pixel_y: int) -> Tuple[float, float]:
        """从物理像素坐标转换为归一化比例 (0.0 - 1.0)。"""
        x_ratio = round(pixel_x / self.width, 4)
        y_ratio = round(pixel_y / self.height, 4)
        return x_ratio, y_ratio

    @classmethod
    def from_wm_size(cls, wm_size_str: str):
        """解析 ADB 'wm size' 输出并创建实例。"""
        try:
            size_part = wm_size_str.split(":")[-1].strip()
            w, h = map(int, size_part.lower().split("x"))
            return cls(w, h)
        except Exception as e:
            logger.error(f"解析屏幕分辨率失败: {wm_size_str}, 错误: {e}")
            raise ValueError("无法解析设备分辨率数据")
