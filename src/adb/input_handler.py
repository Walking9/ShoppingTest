from typing import Dict, Optional
from loguru import logger
from src.adb.transformer import CoordinateTransformer

class InputHandler:
    """封装 ADB 原子触控操作（点击、滑动、长按）。"""

    def __init__(self, device, transformer: Optional[CoordinateTransformer] = None):
        """
        :param device: ppadb 的 Device 对象
        :param transformer: 坐标转换器实例
        """
        self.device = device
        self.transformer = transformer

    def _execute_shell(self, cmd: str):
        if not self.device:
            raise RuntimeError("设备未连接，无法执行指令")
        return self.device.shell(cmd)

    def click(self, x: int, y: int):
        """物理坐标点击。"""
        logger.debug(f"物理点击: ({x}, {y})")
        self._execute_shell(f"input tap {x} {y}")

    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration_ms: int = 300):
        """物理坐标滑动。"""
        logger.debug(f"物理滑动: ({x1}, {y1}) -> ({x2}, {y2}), 耗时: {duration_ms}ms")
        self._execute_shell(f"input swipe {x1} {y1} {x2} {y2} {duration_ms}")

    def long_press(self, x: int, y: int, duration_ms: int = 1000):
        """物理坐标长按（利用滑动起始点相同的原理实现）。"""
        logger.debug(f"物理长按: ({x}, {y}), 耗时: {duration_ms}ms")
        # ADB 'swipe' 命令如果起点和终点相同，耗时即为长按时间
        self.swipe(x, y, x, y, duration_ms)

    # --- 归一化接口 ---

    def click_normalized(self, x_ratio: float, y_ratio: float):
        """归一化比例坐标点击。"""
        if not self.transformer:
            raise ValueError("转换器未初始化，无法使用归一化点击")
        
        pixel = self.transformer.normalize_to_pixel(x_ratio, y_ratio)
        self.click(pixel['x'], pixel['y'])

    def swipe_normalized(self, x1_r: float, y1_r: float, x2_r: float, y2_r: float, duration_ms: int = 300):
        """归一化比例坐标滑动。"""
        if not self.transformer:
            raise ValueError("转换器未初始化，无法使用归一化滑动")
        
        p1 = self.transformer.normalize_to_pixel(x1_r, y1_r)
        p2 = self.transformer.normalize_to_pixel(x2_r, y2_r)
        self.swipe(p1['x'], p1['y'], p2['x'], p2['y'], duration_ms)
