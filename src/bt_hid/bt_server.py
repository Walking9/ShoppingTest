import os
import sys
import time
import socket
import dbus
import dbus.service
import dbus.mainloop.glib
from gi.repository import GLib

# --- 标准 HID 描述符 (Digitizer/触控屏模式) ---
HID_DESCRIPTOR = bytes([
    0x05, 0x0d, 0x09, 0x04, 0xa1, 0x01, 0x85, 0x01, 0x09, 0x42, 0x15, 0x00, 0x25, 0x01, 0x75, 0x01,
    0x95, 0x01, 0x81, 0x02, 0x95, 0x07, 0x81, 0x03, 0x05, 0x01, 0x09, 0x30, 0x09, 0x31, 0x16, 0x00,
    0x00, 0x26, 0xff, 0x7f, 0x75, 0x10, 0x95, 0x02, 0x81, 0x02, 0xc0
])

class BT_HID_Server(dbus.service.Object):
    def __init__(self):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self.bus = dbus.SystemBus()
        self.profile_path = "/test/bt_hid_profile"
        self.hid_uuid = "00001124-0000-1000-8000-00805f9b34fb"
        
        self._setup_profile()
        self._setup_sockets()

    def _setup_profile(self):
        """注册 HID Profile 到 BlueZ。"""
        manager = dbus.Interface(self.bus.get_object("org.bluez", "/org/bluez"), "org.bluez.ProfileManager1")
        
        # 构造 SDP 记录 (XML 格式)
        desc_hex = "".join(["%02x" % b for b in HID_DESCRIPTOR])
        service_record = f"""
        <?xml version="1.0" encoding="UTF-8" ?>
        <record>
          <attribute id="0x0001">
            <sequence><uuid value="{self.hid_uuid}" /></sequence>
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
          <attribute id="0x0201"><uint16 value="0x0111" /></attribute>
          <attribute id="0x0205"><uint16 value="0x0001" /></attribute>
          <attribute id="0x0206">
            <sequence><sequence><uint8 value="0x22" /><text value="{desc_hex}" /></sequence></sequence>
          </attribute>
        </record>
        """
        
        print("--- Registering HID Profile... ---")
        try:
            manager.UnregisterProfile(self.profile_path)
        except:
            pass
            
        manager.RegisterProfile(self.profile_path, self.hid_uuid, {
            "Role": "server",
            "ServiceRecord": service_record,
            "RequireAuthentication": dbus.Boolean(False),
            "RequireAuthorization": dbus.Boolean(False),
        })
        print("Profile Registered.")

    def _setup_sockets(self):
        """绑定 L2CAP 端口。"""
        self.scontrol = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_SEQPACKET, socket.BTPROTO_L2CAP)
        self.sinterrupt = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_SEQPACKET, socket.BTPROTO_L2CAP)
        self.scontrol.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sinterrupt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.scontrol.bind((socket.BDADDR_ANY, 17))
            self.sinterrupt.bind((socket.BDADDR_ANY, 19))
            print("Sockets Bound (PSM 17/19).")
        except OSError as e:
            print(f"FATAL: Socket bind failed: {e}")
            print("HINT: Run 'sudo lsof -i :17' to see who is using the port.")
            sys.exit(1)

    def listen(self):
        self.scontrol.listen(1)
        self.sinterrupt.listen(1)
        
        print("\n--- STANDBY: WAITING FOR PHONE TO CONNECT ---")
        print("Step 1: On phone, UNPAIR/FORGET the computer.")
        print("Step 2: On phone, SCAN and RE-PAIR the computer.")
        
        self.scontrol.settimeout(None)
        self.ccontrol, cinfo = self.scontrol.accept()
        print(f"--- SUCCESS: Control Channel Connected by {cinfo} ---")
        
        self.cinterrupt, cinfo = self.sinterrupt.accept()
        print(f"--- SUCCESS: Interrupt Channel Connected by {cinfo} ---")

    def send_click(self, x=16384, y=16384):
        """发送触控包。"""
        # Down
        report = bytearray([0xa1, 0x01, 0x01, x & 0xFF, (x >> 8) & 0xFF, y & 0xFF, (y >> 8) & 0xFF])
        self.cinterrupt.send(report)
        time.sleep(0.1)
        # Up
        report = bytearray([0xa1, 0x01, 0x00, x & 0xFF, (x >> 8) & 0xFF, y & 0xFF, (y >> 8) & 0xFF])
        self.cinterrupt.send(report)

if __name__ == "__main__":
    server = BT_HID_Server()
    try:
        server.listen()
        while True:
            print("Testing HID Click at center...")
            server.send_click()
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nShutdown.")
