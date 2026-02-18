from src.adb.device_manager import DeviceManager
from src.ocr.screen_capture import ScreenCapturer
from src.utils.config_loader import load_config
from loguru import logger
import os

def verify_physical_capture():
    # 1. 创建日志目录
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # 2. 加载配置并连接设备
    try:
        config = load_config()
    except Exception:
        config = {"adb_host": "127.0.0.1", "adb_port": 5037, "device_serial": ""}

    manager = DeviceManager(host=config['adb_host'], port=config['adb_port'])
    logger.info("正在连接手机进行截图测试...")
    
    if not manager.connect(serial=config.get('device_serial')):
        logger.error("连接失败，请确保手机已连接。")
        return

    # 3. 初始化截图器
    capturer = ScreenCapturer(manager.device)

    # 4. 执行截图并保存
    logger.info("正在截取当前屏幕...")
    img = capturer.capture()
    
    if img is not None:
        save_path = "logs/verify_screen.png"
        capturer.save_last_capture(img, save_path)
        logger.success(f"验证成功！截图已保存至: {save_path}")
        logger.info(f"图像尺寸: {img.shape[1]}x{img.shape[0]}, 通道数: {img.shape[2]}")
        print(f"\n🎉 请在 Finder 中打开: {os.path.abspath(save_path)} 查看图片。")
    else:
        logger.error("截图失败，请检查手机状态。")

if __name__ == "__main__":
    verify_physical_capture()
