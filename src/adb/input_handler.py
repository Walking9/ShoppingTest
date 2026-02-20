import random
import time
import numpy as np
from typing import Dict, Optional, List, Any
from loguru import logger

class InputHandler:
    """高级 ADB 触控封装，针对高风控 App 进行模拟优化。"""

    def __init__(self, device, transformer: Optional[Any] = None):
        self.device = device
        self.transformer = transformer

    def _execute_shell(self, cmd: str):
        if not self.device:
            raise RuntimeError("设备未连接")
        return self.device.shell(cmd)

    def _apply_stealth_offset(self, x: int, y: int, level: int = 2) -> Dict[str, int]:
        sigma = 1.0 + (level * 0.5) 
        dx = int(np.random.normal(0, sigma))
        dy = int(np.random.normal(0, sigma))
        return {"x": x + dx, "y": y + dy}

    def click(self, x: int, y: int, level: int = 2):
        """模拟真人生理特征的‘幽灵点击’。
        通过微小的位移模拟手指触碰屏幕时的滚动。
        """
        target = self._apply_stealth_offset(x, y, level)
        
        # 模拟手指落点的微小滚动 (1-3 像素)
        x2 = target['x'] + random.randint(-1, 1)
        y2 = target['y'] + random.randint(-1, 1)
        
        # 随机按压时长 (80ms - 180ms)
        duration = random.randint(80, 180)
        
        logger.debug(f"[GhostClick L{level}] -> {target} to ({x2}, {y2}) in {duration}ms")
        
        # 使用极短位移的 swipe 替代 tap
        self._execute_shell(f"input swipe {target['x']} {target['y']} {x2} {y2} {duration}")

    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration_ms: int = 350, level: int = 2):
        """带有生理曲线特征的随机滑动。"""
        p1 = self._apply_stealth_offset(x1, y1, level)
        p2 = self._apply_stealth_offset(x2, y2, level)
        
        # 模拟真人滑动：先慢-快-再慢 (通过增加一个中间点实现)
        mid_x = (p1['x'] + p2['x']) // 2 + random.randint(-10, 10)
        mid_y = (p1['y'] + p2['y']) // 2 + random.randint(-10, 10)
        
        real_duration = duration_ms + random.randint(-30, 30)
        
        logger.debug(f"[GhostSwipe L{level}] {p1} -> {p2} (via mid) {real_duration}ms")
        
        # 复杂的滑动目前受限于 adb input 命令，我们采用分段滑动或模拟
        # 在非 Root 下，最稳妥的是带随机持续时间的 swipe
        self._execute_shell(f"input swipe {p1['x']} {p1['y']} {p2['x']} {p2['y']} {real_duration}")

    def click_normalized(self, x_ratio: float, y_ratio: float, level: int = 2):
        if not self.transformer: raise ValueError("转换器未初始化")
        pixel = self.transformer.normalize_to_pixel(x_ratio, y_ratio)
        self.click(pixel['x'], pixel['y'], level=level)

    def sleep_stealth(self, seconds: float, level: int = 2):
        jitter = 0.1 * level
        actual_delay = max(0.05, seconds + random.uniform(-jitter, jitter))
        time.sleep(actual_delay)

    @staticmethod
    def check_environment_risks():
        """输出环境风险警告。"""
        logger.warning("--- 风控对抗检查清单 ---")
        print("1. [ ] 必须关闭 '指针位置' (Pointer Location)！！")
        print("2. [ ] 建议切换至 '无线 ADB' 模式并拔掉数据线。")
        print("3. [ ] 如果手机有 Root，请确保对 i茅台 开启了 Shamiko 隐藏。")
        print("4. [ ] 尝试在启动脚本前，先手动在手机上打开一次 App。")
        print("-----------------------")
