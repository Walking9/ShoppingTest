import os
import sys
import time
import socket
import dbus
import dbus.service
import dbus.mainloop.glib
try:
    from gi.repository import GLib
except ImportError:
    print("Error: Missing 'PyGObject' (python3-gi). Please install it.")
    sys.exit(1)

# --- HID 报告描述符 (Report Descriptor) ---
# 定义为支持绝对坐标的触控屏 (Digitizer)
HID_DESCRIPTOR = bytes([
    0x05, 0x0d,        # USAGE_PAGE (Digitizers)
    0x09, 0x04,        # USAGE (Touch Screen)
    0xa1, 0x01,        # COLLECTION (Application)
    0x85, 0x01,        #   REPORT_ID (1)
    0x09, 0x42,        #   USAGE (Tip Switch)
    0x15, 0x00,        #   LOGICAL_MINIMUM (0)
    0x25, 0x01,        #   LOGICAL_MAXIMUM (1)
    0x75, 0x01,        #   REPORT_SIZE (1)
    0x95, 0x01,        #   REPORT_COUNT (1)
    0x81, 0x02,        #   INPUT (Data,Var,Abs)
    0x95, 0x07,        #   REPORT_COUNT (7)
    0x81, 0x03,        #   INPUT (Cnst,Var,Abs)
    0x05, 0x01,        #   USAGE_PAGE (Generic Desktop)
    0x09, 0x30,        #   USAGE (X)
    0x09, 0x31,        #   USAGE (Y)
    0x16, 0x00, 0x00,  #   LOGICAL_MINIMUM (0)
    0x26, 0xff, 0x7f,  #   LOGICAL_MAXIMUM (32767)
    0x75, 0x10,        #   REPORT_SIZE (16)
    0x95, 0x02,        #   REPORT_COUNT (2)
    0x81, 0x02,        #   INPUT (Data,Var,Abs)
    0xc0               # END_COLLECTION
])

class BT_HID_Server(dbus.service.Object):
    def __init__(self):
        # 1. DBus 初始化
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self.bus = dbus.SystemBus()
        self.adapter_path = "/org/bluez/hci0"
        
        # 2. 注册 HID Profile
        self.manager = dbus.Interface(self.bus.get_object("org.bluez", "/org/bluez"), "org.bluez.ProfileManager1")
        self.profile_path = "/test/bt_hid_profile"
        
        # 构建 XML SDP 记录
        self.service_record = self._generate_sdp_record()
        
        print("Registering HID Profile...")
        self.manager.RegisterProfile(self.profile_path, "00001124-0000-1000-8000-00805f9b34fb", {
            "Role": "server",
            "ServiceRecord": self.service_record,
            "RequireAuthentication": dbus.Boolean(False),
            "RequireAuthorization": dbus.Boolean(False),
        })
        
        # 3. Socket 准备
        self.scontrol = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_SEQPACKET, socket.BTPROTO_L2CAP)
        self.sinterrupt = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_SEQPACKET, socket.BTPROTO_L2CAP)
        
        # 允许端口重用，防止 "Address already in use"
        self.scontrol.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sinterrupt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.ccontrol = None
        self.cinterrupt = None

    def _generate_sdp_record(self):
        desc_hex = "".join(["%02x" % b for b in HID_DESCRIPTOR])
        # 使用标准的 SDP XML 格式，注意十六进制前缀
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
        # 注意：BlueZ XML 模板中的十六进制处理比较特殊，有时需要原始字节
        return xml_template.replace("{descriptor}", desc_hex)

    def listen(self):
        try:
            self.scontrol.bind((socket.BDADDR_ANY, 17))
            self.sinterrupt.bind((socket.BDADDR_ANY, 19))
        except OSError as e:
            print(f"Error binding sockets: {e}")
            print("Make sure you run with sudo and 'bluetoothd --noplugin=input' is active.")
            sys.exit(1)

        self.scontrol.listen(1)
        self.sinterrupt.listen(1)
        
        print("Waiting for phone to connect (PSM 17/19)...")
        self.ccontrol, cinfo = self.scontrol.accept()
        print(f"Control Channel connected by {cinfo}")
        
        self.cinterrupt, cinfo = self.sinterrupt.accept()
        print(f"Interrupt Channel connected by {cinfo}")

    def send_report(self, down=False, x=0, y=0):
        if not self.cinterrupt:
            return
        state = 0x01 if down else 0x00
        x_val = int(x) & 0x7FFF
        y_val = int(y) & 0x7FFF
        
        # 构造 HID 报告数据包
        # 0xa1 表示数据输入
        report = bytearray([
            0xa1, 0x01, state,
            x_val & 0xFF, (x_val >> 8) & 0xFF,
            y_val & 0xFF, (y_val >> 8) & 0xFF
        ])
        try:
            self.cinterrupt.send(report)
        except Exception as e:
            print(f"Send failed: {e}")

if __name__ == "__main__":
    server = BT_HID_Server()
    try:
        server.listen()
        while True:
            # 示例：点击屏幕中央
            print("Action: Click Center")
            server.send_report(True, 16384, 16384)
            time.sleep(0.1)
            server.send_report(False, 16384, 16384)
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nShutting down...")
