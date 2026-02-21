import os
import sys
import time
import socket
import dbus
import dbus.service
import dbus.mainloop.glib
from gi.repository import GLib

# --- 自动授权代理 (Bluetooth Agent) ---
# 负责自动点击 "yes" 以允许 HID 连接
class Agent(dbus.service.Object):
    @dbus.service.method("org.bluez.Agent1", in_signature="os", out_signature="")
    def AuthorizeService(self, device, uuid):
        print(f"Auto-Authorizing Service: {uuid} for {device}")
        return

    @dbus.service.method("org.bluez.Agent1", in_signature="o", out_signature="")
    def RequestAuthorization(self, device):
        print(f"Auto-Request-Authorization for {device}")
        return

    @dbus.service.method("org.bluez.Agent1", in_signature="", out_signature="")
    def Release(self):
        print("Agent Release")
        return

def register_agent(bus):
    path = "/test/auto_agent"
    agent = Agent(bus, path)
    obj = bus.get_object("org.bluez", "/org/bluez")
    manager = dbus.Interface(obj, "org.bluez.AgentManager1")
    manager.RegisterAgent(path, "NoInputNoOutput")
    manager.RequestDefaultAgent(path)
    print("Auto-Agent Registered (No more 'yes' needed).")
    return agent

# --- 标准蓝牙鼠标描述符 (Mouse Mode) ---
HID_DESCRIPTOR = bytes([
    0x05, 0x01, 0x09, 0x02, 0xa1, 0x01, 0x09, 0x01, 0xa1, 0x00, 0x05, 0x09, 0x19, 0x01, 0x29, 0x03,
    0x15, 0x00, 0x25, 0x01, 0x95, 0x03, 0x75, 0x01, 0x81, 0x02, 0x95, 0x01, 0x75, 0x05, 0x81, 0x03,
    0x05, 0x01, 0x09, 0x30, 0x09, 0x31, 0x15, 0x81, 0x25, 0x7f, 0x75, 0x08, 0x95, 0x02, 0x81, 0x06,
    0xc0, 0xc0
])

class BT_HID_Server(dbus.service.Object):
    def __init__(self):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self.bus = dbus.SystemBus()
        self.profile_path = "/test/bt_hid_profile"
        self.hid_uuid = "00001124-0000-1000-8000-00805f9b34fb"
        
        # 注册全自动代理
        self.agent = register_agent(self.bus)
        self._setup_profile()
        self._setup_sockets()

    def _setup_profile(self):
        manager = dbus.Interface(self.bus.get_object("org.bluez", "/org/bluez"), "org.bluez.ProfileManager1")
        desc_hex = "".join(["%02x" % b for b in HID_DESCRIPTOR])
        service_record = f"""
        <?xml version="1.0" encoding="UTF-8" ?>
        <record>
          <attribute id="0x0001"><sequence><uuid value="{self.hid_uuid}" /></sequence></attribute>
          <attribute id="0x0004"><sequence><sequence><uuid value="00000100" /><uint16 value="0x0011" /></sequence><sequence><uuid value="00000011" /></sequence></sequence></attribute>
          <attribute id="0x000d"><sequence><sequence><uuid value="00000100" /><uint16 value="0x0013" /></sequence><sequence><uuid value="00000011" /></sequence></sequence></attribute>
          <attribute id="0x0201"><uint16 value="0x0111" /></attribute>
          <attribute id="0x0205"><uint16 value="0x0001" /></attribute>
          <attribute id="0x0206"><sequence><sequence><uint8 value="0x22" /><text value="{desc_hex}" /></sequence></sequence></attribute>
        </record>
        """
        try: manager.UnregisterProfile(self.profile_path)
        except: pass
        manager.RegisterProfile(self.profile_path, self.hid_uuid, {"Role": "server", "ServiceRecord": service_record})

    def _setup_sockets(self):
        self.scontrol = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_SEQPACKET, socket.BTPROTO_L2CAP)
        self.sinterrupt = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_SEQPACKET, socket.BTPROTO_L2CAP)
        self.scontrol.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sinterrupt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.scontrol.bind((socket.BDADDR_ANY, 17))
        self.sinterrupt.bind((socket.BDADDR_ANY, 19))

    def listen(self):
        self.scontrol.listen(1)
        self.sinterrupt.listen(1)
        print("Waiting for phone connection (Auto-Auth Active)...")
        self.ccontrol, _ = self.scontrol.accept()
        self.cinterrupt, _ = self.sinterrupt.accept()
        print("CONNECTED.")

    def move_mouse(self, dx, dy):
        report = bytearray([0xa1, 0x01, 0x00, dx & 0xFF, dy & 0xFF])
        self.cinterrupt.send(report)

if __name__ == "__main__":
    server = BT_HID_Server()
    # 启动后台主循环以处理 Agent 的 D-Bus 请求
    mainloop = GLib.MainLoop()
    import threading
    threading.Thread(target=mainloop.run, daemon=True).start()
    
    try:
        server.listen()
        while True:
            server.move_mouse(20, 0)
            time.sleep(0.05)
            server.move_mouse(-20, 0)
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("\nExit")
