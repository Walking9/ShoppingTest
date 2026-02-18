import cv2
import numpy as np
from loguru import logger
from typing import Optional

class ScreenCapturer:
    """负责从 ADB 设备高效采集屏幕图像并转换为 OpenCV 格式。"""

    def __init__(self, device):
        """
        :param device: ppadb 的 Device 对象
        """
        self.device = device

    def capture(self) -> Optional[np.ndarray]:
        """获取当前屏幕截图并返回为 OpenCV 图像 (NumPy 数组)。"""
        if not self.device:
            logger.error("截图失败: 未连接设备")
            return None

        try:
            # 采用 ppadb 的 screencap()，它直接返回字节流
            raw_bytes = self.device.screencap()
            if not raw_bytes:
                logger.error("截图失败: 获取到的字节流为空")
                return None

            # 将字节流解码为 OpenCV 图像
            # 注意：imdecode 会自动处理不同的图像格式 (通常为 PNG)
            img = cv2.imdecode(np.frombuffer(raw_bytes, np.uint8), cv2.IMREAD_COLOR)
            
            if img is None:
                logger.error("截图失败: 图像解码返回空对象")
                return None
            
            # 记录截图成功（可选，正式运行时可降低日志等级）
            logger.debug(f"截图成功: {img.shape[1]}x{img.shape[0]}")
            return img

        except Exception as e:
            logger.exception(f"截图过程中发生异常: {e}")
            return None

    def save_last_capture(self, img: np.ndarray, path: str = "logs/last_screen.png"):
        """将截图保存到本地，用于调试。"""
        try:
            cv2.imwrite(path, img)
            logger.info(f"截图已保存至: {path}")
        except Exception as e:
            logger.error(f"保存截图失败: {e}")
