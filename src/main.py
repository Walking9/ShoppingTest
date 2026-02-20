import argparse
import sys
from loguru import logger
from src.utils.config_loader import load_config
from src.adb.device_manager import DeviceManager
from src.adb.input_handler import InputHandler
from src.engine.scheduler import WorkflowExecutor
from src.utils.notifier import Notifier

def setup_args():
    parser = argparse.ArgumentParser(description="iMaotai 自动化抢购引擎 (最终闭环版)")
    parser.add_argument("--task", type=str, default="imaotai", help="任务名称")
    parser.add_argument("--serial", type=str, help="ADB 序列号")
    parser.add_argument("--once", action="store_true", help="仅执行一次")
    return parser.parse_args()

def main():
    args = setup_args()
    
    # 1. 加载配置
    try:
        config = load_config()
    except Exception as e:
        logger.error(f"加载配置失败: {e}")
        sys.exit(1)

    serial = args.serial if args.serial else config.get('device_serial')
    send_key = config.get('webhook_url') # Server 酱 SendKey

    # 2. 连接与初始化
    manager = DeviceManager(host=config.get('adb_host', '127.0.0.1'), 
                            port=config.get('adb_port', 5037))
    notifier = Notifier(send_key=send_key)
    
    logger.info("iMaotai 引擎启动中...")
    if not manager.connect(serial=serial):
        notifier.send("iMaotai 启动失败", "无法建立 ADB 连接，请检查物理设备。")
        sys.exit(1)

    # 3. 运行执行引擎
    handler = InputHandler(manager.device, manager.transformer)
    executor = WorkflowExecutor(handler)
    
    try:
        logger.success("--- 任务开始 ---")
        executor.execute(args.task)
        
        # 4. 任务结束通知
        notifier.send(f"iMaotai 任务完成: {args.task}", "所有定义的动作序列已顺序执行完毕。")
            
    except KeyboardInterrupt:
        logger.warning("用户手动中止。")
    except Exception as e:
        logger.exception(f"运行异常: {e}")
        notifier.send("iMaotai 运行异常", str(e))
    finally:
        logger.info("iMaotai 引擎已安全关闭。")

if __name__ == "__main__":
    main()
