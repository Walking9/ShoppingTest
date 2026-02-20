import sys
import os
from loguru import logger

# 确保能导入 src 模块
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(project_root)

from src.adb.device_manager import DeviceManager
from src.utils.config_loader import load_config

def main():
    """
    坐标采集助手：手动输入物理像素坐标，输出归一化 JSON 配置。
    """
    try:
        config = load_config()
    except Exception:
        config = {"adb_host": "127.0.0.1", "adb_port": 5037, "device_serial": ""}

    manager = DeviceManager(host=config.get('adb_host', '127.0.0.1'), 
                            port=config.get('adb_port', 5037))
    
    logger.info("正在连接手机...")
    if not manager.connect(serial=config.get('device_serial')):
        logger.error("连接失败，请检查手机是否正确连接。")
        return

    info = manager.get_device_info()
    
    print("\n" + "="*50)
    print(" iMaotai 坐标采集助手 ".center(50, "="))
    print("="*50)
    print(f"当前设备: {info.get('model')} | 分辨率: {info.get('resolution')}")
    print("\n操作步骤：")
    print("1. 在手机上开启 [设置] -> [开发者选项] -> [指针位置] (Pointer Location)")
    print("2. 记录屏幕顶部显示的 X: 123, Y: 456 数值")
    print("3. 在下方输入记录的数值进行转换")
    print("="*50)

    try:
        while True:
            try:
                line = input("\n请输入 X Y (空格分隔, 或 Ctrl+C 退出): ").strip()
                if not line:
                    continue
                
                parts = line.split()
                if len(parts) != 2:
                    print("❌ 请输入两个数字，例如: 540 1200")
                    continue
                
                x, y = int(parts[0]), int(parts[1])
                
                # 使用 DeviceManager 中已初始化的 transformer 进行转换
                if manager.transformer:
                    x_r, y_r = manager.transformer.pixel_to_normalize(x, y)
                    
                    print(f"\n✅ 转换结果:")
                    print(f"  物理坐标: ({x}, {y})")
                    print(f"  归一化配置: {{\"x_ratio\": {x_r}, \"y_ratio\": {y_r}}}")
                    print(f"  [提示] 复制归一化配置到任务 JSON 中即可。")
                else:
                    print("❌ 错误: 坐标转换器未就绪。")
                    
            except ValueError:
                print("❌ 输入格式有误，请输入纯数字。")
    except KeyboardInterrupt:
        print("\n\n退出采集助手。")

if __name__ == "__main__":
    main()
