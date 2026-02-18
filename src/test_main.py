import unittest
from unittest.mock import MagicMock, patch
import sys

# Mock 外部依赖
mock_ppadb = MagicMock()
sys.modules["ppadb"] = mock_ppadb
sys.modules["ppadb.client"] = mock_ppadb
mock_loguru = MagicMock()
sys.modules["loguru"] = mock_loguru

from src.main import setup_args

class TestMainLauncher(unittest.TestCase):
    def test_argument_parsing(self):
        # 模拟命令行参数
        test_args = ['--task', 'test_task', '--serial', 'TEST1234']
        with patch.object(sys, 'argv', ['main.py'] + test_args):
            args = setup_args()
            self.assertEqual(args.task, 'test_task')
            self.assertEqual(args.serial, 'TEST1234')

    @patch('src.main.DeviceManager')
    @patch('src.main.load_config')
    def test_main_initialization_flow(self, mock_load_config, mock_device_manager):
        # 配置模拟
        mock_load_config.return_value = {
            "device_serial": "CONFIG_SERIAL",
            "adb_host": "127.0.0.1",
            "adb_port": 5037
        }
        
        # 设备管理模拟
        mock_mgr_instance = mock_device_manager.return_value
        mock_mgr_instance.connect.return_value = True
        mock_mgr_instance.get_device_info.return_value = {
            "model": "MockPhone",
            "serial": "CONFIG_SERIAL",
            "resolution": "1080x1920"
        }

        # 我们只需验证它能跑到等待循环之前即可
        # 这里通过 patch time.sleep 来抛出异常提前终止循环
        with patch('time.sleep', side_effect=KeyboardInterrupt):
            from src.main import main
            with patch.object(sys, 'argv', ['main.py']):
                main()
                
        # 验证是否优先使用了配置中的序列号
        mock_mgr_instance.connect.assert_called_with(serial="CONFIG_SERIAL")

if __name__ == "__main__":
    unittest.main()
