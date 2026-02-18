from src.adb.device_manager import DeviceManager
from src.adb.input_handler import InputHandler
from src.utils.config_loader import load_config
from loguru import logger
import time

def verify_physical_actions():
    # 1. 加载配置
    try:
        config = load_config()
    except Exception:
        config = {"adb_host": "127.0.0.1", "adb_port": 5037, "device_serial": ""}

    # 2. 初始化连接
    manager = DeviceManager(host=config['adb_host'], port=config['adb_port'])
    logger.info("正在尝试连接设备...")
    
    if not manager.connect(serial=config.get('device_serial')):
        logger.error("连接失败，请确保手机已连接并开启 USB 调试。")
        return

    # 3. 初始化输入处理器
    handler = InputHandler(manager.device, manager.transformer)

    logger.info("--- 开始物理动作验证 ---")
    logger.info("提示：请确保手机屏幕已点亮并解锁，最好停留在可滚动的页面。")
    time.sleep(2)

    # 测试 A: 屏幕中心归一化点击
    logger.info("测试 1: 执行屏幕中心点击 (0.5, 0.5)...")
    handler.click_normalized(0.5, 0.5)
    time.sleep(1)

    # 测试 B: 归一化向上滑动 (从屏幕 80% 高度滑向 20%)
    logger.info("测试 2: 执行向上滑动 (Swipe Up)...")
    handler.swipe_normalized(0.5, 0.8, 0.5, 0.2, duration_ms=500)
    
    logger.success("动作指令发送完毕！请观察手机是否有相应反应。")

if __name__ == "__main__":
    verify_physical_actions()
