import json
import os
from typing import TypedDict, Any

class AppConfig(TypedDict):
    device_serial: str
    adb_host: str
    adb_port: int
    webhook_url: str
    stealth_level: int

def load_config(config_path: str = "config/settings.json") -> AppConfig:
    """加载并解析本地 JSON 配置文件。"""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"配置文件未找到: {config_path}")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config: AppConfig = json.load(f)
    return config
