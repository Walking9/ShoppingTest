import unittest
from unittest.mock import MagicMock, patch
import sys

# Mock 外部库
mock_ppadb = MagicMock()
sys.modules["ppadb"] = mock_ppadb
sys.modules["ppadb.client"] = mock_ppadb

mock_loguru = MagicMock()
sys.modules["loguru"] = mock_loguru

from src.adb.device_manager import DeviceManager

class TestDeviceManager(unittest.TestCase):
    def test_connect_success(self):
        # 模拟 AdbClient
        mock_client = MagicMock()
        mock_device = MagicMock()
        mock_device.serial = "test_serial"
        mock_client.devices.return_value = [mock_device]
        
        manager = DeviceManager()
        manager.client = mock_client
        result = manager.connect("test_serial")
        
        self.assertTrue(result)
        self.assertEqual(manager.device.serial, "test_serial")

    def test_get_device_info(self):
        mock_client = MagicMock()
        mock_device = MagicMock()
        mock_device.serial = "test_serial"
        mock_device.shell.side_effect = ["Redmi K40", "Physical size: 1080x2400"]
        mock_client.devices.return_value = [mock_device]
        
        manager = DeviceManager()
        manager.client = mock_client
        manager.connect("test_serial")
        info = manager.get_device_info()
        
        self.assertEqual(info['model'], "Redmi K40")
        self.assertEqual(info['resolution'], "1080x2400")

if __name__ == "__main__":
    unittest.main()
