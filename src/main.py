import argparse
import sys
from loguru import logger
from src.utils.config_loader import load_config
from src.adb.device_manager import DeviceManager
from src.adb.input_handler import InputHandler

def setup_args():
    parser = argparse.ArgumentParser(description="iMaotai 自动化抢购引擎")
    parser.add_argument("--task", type=str, default="imaotai", help="指定抢购任务 JSON 名称")
    parser.add_argument("--serial", type=str, help="覆盖配置文件中的设备序列号")
    parser.add_argument("--debug", action="store_true", help="开启调试模式")
    return parser.parse_args()

def main():
    args = setup_args()
    
    # 1. 加载配置
    try:
        config = load_config()
    except Exception as e:
        logger.error(f"配置文件加载失败: {e}")
        sys.exit(1)

    # 命令行参数覆盖
    serial = args.serial if args.serial else config.get('device_serial')

    # 2. 初始化设备管理
    manager = DeviceManager(host=config.get('adb_host', '127.0.0.1'), 
                            port=config.get('adb_port', 5037))
    
    logger.info("iMaotai 引擎正在启动...")
    
    if not manager.connect(serial=serial):
        logger.error("无法建立 ADB 连接，程序退出。")
        sys.exit(1)

    # 3. 准备运行环境摘要
    device_info = manager.get_device_info()
    logger.success("--- 引擎准备就绪 ---")
    logger.info(f"目标设备: {device_info['model']} ({device_info['serial']})")
    logger.info(f"屏幕尺寸: {device_info['resolution']}")
    logger.info(f"当前任务: {args.task}")
    logger.info(f"防御等级: {config.get('stealth_level', 2)}")
    
    # 4. 初始化处理器（为后续 Epic 准备）
    handler = InputHandler(manager.device, manager.transformer)
    
    try:
        logger.info("等待任务调度... (按 Ctrl+C 停止)")
        # 此处为 Epic 3 的执行入口预留位置
        # run_engine(handler, args.task)
        while True:
            # 暂时保持运行以验证连接稳定性
            import time
            time.sleep(10)
    except KeyboardInterrupt:
        logger.warning("用户请求停止，正在清理资源...")
    finally:
        logger.info("iMaotai 引擎已安全关闭。")

if __name__ == "__main__":
    main()
