from ppadb.client import Client as AdbClient
from loguru import logger
from typing import Dict, Any, Optional
from src.utils.config_loader import load_config
from src.adb.transformer import CoordinateTransformer

class DeviceManager:
    def __init__(self, host: str = "127.0.0.1", port: int = 5037):
        self.client = AdbClient(host=host, port=port)
        self.device = None
        self.transformer: Optional[CoordinateTransformer] = None

    def connect(self, serial: Optional[str] = None):
        """连接到指定的 ADB 设备。"""
        try:
            devices = self.client.devices()
            if not devices:
                logger.error("未检测到任何 ADB 设备，请确保 adb server 已启动。")
                return False
            
            if serial:
                self.device = next((d for d in devices if d.serial == serial), None)
            else:
                self.device = devices[0]
            
            if not self.device:
                logger.error(f"未找到序列号为 {serial} 的设备。")
                return False
            
            logger.info(f"成功连接到设备: {self.device.serial}")
            
            # 自动初始化坐标转换器
            wm_size_str = self.device.shell("wm size")
            self.transformer = CoordinateTransformer.from_wm_size(wm_size_str)
            
            return True
        except Exception as e:
            logger.exception(f"ADB 连接异常: {e}")
            return False

    def get_device_info(self) -> Dict[str, Any]:
        """提取设备型号与屏幕分辨率。"""
        if not self.device:
            return {}
        
        model = self.device.shell("getprop ro.product.model").strip()
        size_str = self.device.shell("wm size").strip()
        resolution = size_str.split(":")[-1].strip() if ":" in size_str else "Unknown"
        
        return {
            "serial": self.device.serial,
            "model": model,
            "resolution": resolution
        }
