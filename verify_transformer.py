from src.adb.device_manager import DeviceManager
from src.utils.config_loader import load_config
from loguru import logger

def verify():
    # 1. 加载配置（请确保 config/settings.json 中 device_serial 已填入，或留空连接首个设备）
    try:
        config = load_config()
    except Exception:
        config = {"adb_host": "127.0.0.1", "adb_port": 5037, "device_serial": ""}

    # 2. 初始化设备管理
    manager = DeviceManager(host=config['adb_host'], port=config['adb_port'])
    
    logger.info("正在尝试连接物理设备...")
    if not manager.connect(serial=config.get('device_serial')):
        logger.error("连接失败，请检查 ADB 连接和设置。")
        return

    # 3. 获取并打印设备信息
    info = manager.get_device_info()
    
    # 4. 验证坐标转换
    if manager.transformer:
        # 测试屏幕中心点 (0.5, 0.5)
        center_pixel = manager.transformer.normalize_to_pixel(0.5, 0.5)
        logger.success(f"验证成功！")
        logger.info(f"屏幕分辨率: {info['resolution']}")
        logger.info(f"归一化中心点 (0.5, 0.5) 对应的物理像素坐标为: {center_pixel}")
        
        print("
--- 请手动比对 ---")
        w, h = map(int, info['resolution'].lower().split('x'))
        expected_x, expected_y = w // 2, h // 2
        print(f"预期手动计算中心点: {{'x': {expected_x}, 'y': {expected_y}}}")
        print(f"转换器计算中心点: {center_pixel}")
        
        if center_pixel['x'] == expected_x and center_pixel['y'] == expected_y:
            print("
✅ 结果一致！坐标归一化工具在物理设备上运行完美。")
        else:
            print("
❌ 结果不一致，请检查分辨率解析逻辑。")
    else:
        logger.error("转换器未初始化。")

if __name__ == "__main__":
    verify()
