import pty, subprocess, sys, os, pty
from enum import Enum

class WarpStatus(Enum):
    CONNECTED = "Connected"
    DISCONNECTED = "Disconnected"

class Warp:
    def _register(self):
        master, slave = pty.openpty()
        register_warp_result = subprocess.Popen(
            ["warp-cli", "registration", "new"],
            stdin=slave,
            stdout=slave,
            stderr=slave
        )
        os.close(slave)
        os.write(master, "yes\n".encode())
        register_warp_result.wait(timeout=10)
        os.close(master)
        
        if register_warp_result.returncode == 0:
            print("Warp was registered successfully!")
        else:
            print("Warp registration failed!")
            sys.exit(1)

    def _set_mode(self):
        set_warp_mode_result = subprocess.run(
            ["warp-cli", "mode", "proxy"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        if set_warp_mode_result.returncode == 0:
            print(f"Warp mode set to proxy")

    def connect(self):
        connect_warp_result = subprocess.run(
            ["warp-cli", "connect"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        if connect_warp_result.returncode != 0:
            print("Warp connection failed!")
            sys.exit(1)
            
    def enable_warp_tunnel(self, enable_warp: bool):
        if not enable_warp:
            print("Warp is disabled. Skipping Warp connection.")
            return
        
        self._register()
        self._set_mode()
        self.connect()
        
    def disconnect(self):
        disconnect_warp_result = subprocess.run(
            ["warp-cli", "disconnect"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        if disconnect_warp_result.returncode == 0:
            print("Warp disconnected successfully!")

    def status(self):
        status_warp_result = subprocess.run(
            ["warp-cli", "status"],
            capture_output=True,
            text=True
        )
        if WarpStatus.CONNECTED.value in status_warp_result.stdout:
            return WarpStatus.CONNECTED
        return WarpStatus.DISCONNECTED

    def unregister(self):
        unregister_warp_result = subprocess.run(
            ["warp-cli", "registration", "delete"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        if unregister_warp_result.returncode == 0:
            print("Warp unregistered successfully!")