import json
import os
import time
from loguru import logger
from src.adb.input_handler import InputHandler

class WorkflowExecutor:
    """负责加载并顺序执行 JSON 定义的任务流。"""

    def __init__(self, input_handler: InputHandler):
        self.handler = input_handler
        self.workflow_dir = "config/workflows"

    def load_steps(self, task_name: str):
        """从 JSON 文件加载动作步骤。"""
        file_path = os.path.join(self.workflow_dir, f"{task_name}_flow.json")
        if not os.path.exists(file_path):
            logger.error(f"任务文件不存在: {file_path}")
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"解析任务文件失败: {e}")
            return None

    def execute(self, task_name: str):
        """开始执行指定的任务。"""
        steps = self.load_steps(task_name)
        if not steps:
            return

        logger.info(f"开始执行任务序列: {task_name} (共 {len(steps)} 步)")
        
        for i, step in enumerate(steps):
            step_name = step.get('name', f"步骤 {i+1}")
            action = step.get('action')
            delay = step.get('delay_after', 1.0)
            # 获取步骤特有的防御等级，默认为 2
            level = step.get('stealth_level', 2)
            
            logger.info(f"[Step {i+1}] 执行: {step_name} (Level {level})...")
            
            try:
                # 拟人化随机“观察屏幕”延迟 (1.2s - 3.5s)
                # 只有从第二步开始才需要这个延迟，第一步(打开App)不需要
                if i > 0:
                    import random
                    obs_delay = random.uniform(1.2, 3.5)
                    logger.debug(f"正在观察屏幕... ({obs_delay:.2f}s)")
                    time.sleep(obs_delay)

                if action == "click":
                    self.handler.click_normalized(step['x_ratio'], step['y_ratio'], level=level)
                
                elif action == "swipe":
                    self.handler.swipe_normalized(
                        step['start_x_ratio'], step['start_y_ratio'],
                        step['end_x_ratio'], step['end_y_ratio'],
                        duration_ms=step.get('duration_ms', 300),
                        level=level
                    )
                
                else:
                    logger.warning(f"未知动作: {action}")
                
                if delay > 0:
                    self.handler.sleep_stealth(delay, level=level)
                    
            except KeyError as e:
                logger.error(f"步骤配置缺失必填字段: {e}")
                break
            except Exception as e:
                logger.exception(f"步骤执行发生异常: {e}")
                break
        
        logger.success(f"任务序列 {task_name} 执行完毕。")
