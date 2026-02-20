import os
import sys
import time
import socket
import dbus
import dbus.service
import dbus.mainloop.glib
from gi.repository import GLib

# --- HID 报告描述符 (Report Descriptor) ---
# 定义为支持绝对坐标的触控屏 (Digitizer)
# 这能让你直接发送像素坐标给手机，不需要相对移动。
HID_DESCRIPTOR = (
    "\x05\x0d"        # USAGE_PAGE (Digitizers)
    "\x09\x04"        # USAGE (Touch Screen)
    "\xa1\x01"        # COLLECTION (Application)
    "\x85\x01"        #   REPORT_ID (1)
    "\x09\x42"        #   USAGE (Tip Switch)
    "\x15\x00"        #   LOGICAL_MINIMUM (0)
    "\x25\x01"        #   LOGICAL_MAXIMUM (1)
    "\x75\x01"        #   REPORT_SIZE (1)
    "\x95\x01"        #   REPORT_COUNT (1)
    "\x81\x02"        #   INPUT (Data,Var,Abs)
    "\x95\x07"        #   REPORT_COUNT (7)
    "\x81\x03"        #   INPUT (Cnst,Var,Abs)
    "\x05\x01"        #   USAGE_PAGE (Generic Desktop)
    "\x09\x30"        #   USAGE (X)
    "\x09\x31"        #   USAGE (Y)
    "\x16\x00\x00"    #   LOGICAL_MINIMUM (0)
    "\x26\xff\x7f"    #   LOGICAL_MAXIMUM (32767) - 绝对坐标最大范围
    "\x75\x10"        #   REPORT_SIZE (16)
    "\x95\x02"        #   REPORT_COUNT (2)
    "\x81\x02"        #   INPUT (Data,Var,Abs)
    "\xc0"            # END_COLLECTION
)

class BT_HID_Server(dbus.service.Object):
    def __init__(self):
        # 1. DBus 初始化，用于注册 SDP 记录
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self.bus = dbus.SystemBus()
        self.adapter_path = "/org/bluez/hci0"
        self.service_record = self._load_sdp_record()
        
        # 2. 注册 HID Profile 到 BlueZ
        self.manager = dbus.Interface(self.bus.get_object("org.bluez", "/org/bluez"), "org.bluez.ProfileManager1")
        self.profile_path = "/test/bt_hid_profile"
        self.manager.RegisterProfile(self.profile_path, "00001124-0000-1000-8000-00805f9b34fb", {
            "Role": "server",
            "ServiceRecord": self.service_record
        })
        
        # 3. L2CAP Socket 初始化 (PSM 17: Control, PSM 19: Interrupt)
        self.scontrol = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_SEQPACKET, socket.BTPROTO_L2CAP)
        self.sinterrupt = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_SEQPACKET, socket.BTPROTO_L2CAP)
        
        self.ccontrol = None
        self.cinterrupt = None

    def _load_sdp_record(self):
        """生成符合 HID 协议的 XML SDP 记录。"""
        # 这里为了演示简洁，使用硬编码的 XML 片段
        # 在生产代码中通常会从模板生成
        with open("_bmad/bmm/testarch/knowledge/api-request.md", "r") as f: # 临时借用路径逻辑，实际直接定义
             pass
        # 核心 XML 见下
        xml_template = """
        <?xml version="1.0" encoding="UTF-8" ?>
        <record>
          <attribute id="0x0001">
            <sequence><uuid value="00001124-0000-1000-8000-00805f9b34fb" /></sequence>
          </attribute>
          <attribute id="0x0004">
            <sequence>
              <sequence><uuid value="00000100" /><uint16 value="0x0011" /></sequence>
              <sequence><uuid value="00000011" /></sequence>
            </sequence>
          </attribute>
          <attribute id="0x000d">
            <sequence>
              <sequence><uuid value="00000100" /><uint16 value="0x0013" /></sequence>
              <sequence><uuid value="00000011" /></sequence>
            </sequence>
          </attribute>
          <attribute id="0x0201">
            <uint16 value="0x0111" />
          </attribute>
          <attribute id="0x0205">
            <uint16 value="0x0001" />
          </attribute>
          <attribute id="0x0206">
            <sequence><sequence><uint8 value="0x22" /><text value="{descriptor}" /></sequence></sequence>
          </attribute>
        </record>
        """
        # 将描述符转义为 XML 文本
        desc_hex = "".join(["\x%02x" % ord(c) for c in HID_DESCRIPTOR])
        return xml_template.replace("{descriptor}", desc_hex)

    def listen(self):
        """监听手机连接请求。"""
        # PSM 17 (Control)
        self.scontrol.bind((socket.BDADDR_ANY, 17))
        self.scontrol.listen(1)
        # PSM 19 (Interrupt)
        self.sinterrupt.bind((socket.BDADDR_ANY, 19))
        self.sinterrupt.listen(1)
        
        print("--- HID Server Started. Waiting for Phone Connection... ---")
        print("1. Please pair your phone with Ubuntu via bluetoothctl.")
        print("2. Once paired, the phone should automatically connect to this HID service.")
        
        self.ccontrol, cinfo = self.scontrol.accept()
        print(f"Control Channel connected by {cinfo}")
        
        self.cinterrupt, cinfo = self.sinterrupt.accept()
        print(f"Interrupt Channel connected by {cinfo}")

    def send_report(self, down=False, x=0, y=0):
        """发送触控报告。"""
        if not self.cinterrupt:
            return
            
        # 报文格式: [Header, ReportID, TipSwitch, X_Low, X_High, Y_Low, Y_High]
        # 0xa1 是 HID 数据包头
        state = 0x01 if down else 0x00
        # X, Y 范围映射到 0-32767
        x_val = int(x) & 0x7FFF
        y_val = int(y) & 0x7FFF
        
        report = bytearray([
            0xa1, # DATA Input
            0x01, # Report ID
            state,
            x_val & 0xFF, (x_val >> 8) & 0xFF,
            y_val & 0xFF, (y_val >> 8) & 0xFF
        ])
        self.cinterrupt.send(report)

if __name__ == "__main__":
    server = BT_HID_Server()
    try:
        server.listen()
        # 测试点击中心点
        print("Clicking Center (16384, 16384)...")
        server.send_report(True, 16384, 16384)
        time.sleep(0.1)
        server.send_report(False, 16384, 16384)
        
        # 保持连接，以便你可以手动测试
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("
Shutting down...")
