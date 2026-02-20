import requests
from loguru import logger
from typing import Optional

class Notifier:
    """负责将执行结果通过 Webhook (Server酱) 推送到用户。"""

    def __init__(self, send_key: Optional[str] = None):
        """
        :param send_key: Server 酱的 SendKey
        """
        self.send_key = send_key
        self.api_url = f"https://sctapi.ftqq.com/{send_key}.send" if send_key else None

    def send(self, title: str, content: str = ""):
        """发送通知。"""
        if not self.send_key:
            logger.warning("未配置 Server 酱 SendKey，跳过通知发送。")
            return False

        data = {
            "title": title,
            "desp": content
        }

        try:
            logger.info(f"正在发送远程通知: {title}")
            response = requests.post(self.api_url, data=data, timeout=10)
            result = response.json()
            
            if result.get("code") == 0:
                logger.success("通知发送成功。")
                return True
            else:
                logger.error(f"通知发送失败: {result.get('message')}")
                return False
        except Exception as e:
            logger.error(f"通知接口请求异常: {e}")
            return False
