from src.adb.device_manager import DeviceManager
from src.ocr.screen_capture import ScreenCapturer
from src.ocr.pre_processor import ImageProcessor
from src.utils.config_loader import load_config
from loguru import logger
import os

def visualize():
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # 1. 连接设备
    try:
        config = load_config()
    except Exception:
        config = {"adb_host": "127.0.0.1", "adb_port": 5037, "device_serial": ""}

    manager = DeviceManager(host=config['adb_host'], port=config['adb_port'])
    if not manager.connect(serial=config.get('device_serial')):
        logger.error("设备连接失败。")
        return

    # 2. 采样原始截图
    capturer = ScreenCapturer(manager.device)
    raw_img = capturer.capture()
    if raw_img is None:
        return

    # 3. 运行预处理
    processor = ImageProcessor()
    
    # 灰度处理效果
    gray_img = processor.to_gray(raw_img)
    # 降噪+二值化效果
    binary_img = processor.process_for_ocr(raw_img, use_binary=True)

    # 4. 保存结果
    processor.save_debug_img(gray_img, "1_gray")
    processor.save_debug_img(binary_img, "2_binary")

    logger.success("可视化任务完成！")
    print(f"📸 请检查 logs/ 目录下的两张图片：")
    print(f"1. logs/debug_1_gray.png   (灰度降噪版)")
    print(f"2. logs/debug_2_binary.png (黑白高对比版)")
    print(f"提示：如果黑白图中的文字很清晰，则说明识别率会非常高。")

if __name__ == "__main__":
    visualize()
