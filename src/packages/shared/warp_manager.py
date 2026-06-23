import pty, subprocess, sys, os, pty, time
from enum import Enum
from shared.logger import Logger

class WarpStatus(Enum):
    CONNECTED = "Connected"
    DISCONNECTED = "Disconnected"
    CONNECTION_FAILED = "Connection Failed"

class WarpManager:
    def __init__(self):
        self.logger = Logger("WarpManager")

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
            self.logger.info("Warp was registered successfully!")
        else:
            self.logger.error("Warp registration failed!")
            sys.exit(1)

    def _set_mode(self):
        set_warp_mode_result = subprocess.run(
            ["warp-cli", "mode", "proxy"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        if set_warp_mode_result.returncode != 0:
            self.logger.error("Failed to set Warp mode!")
            sys.exit(1)

    def connect(self):
        connect_warp_result = subprocess.run(
            ["warp-cli", "connect"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        if connect_warp_result.returncode == 0:
            self.logger.info("Warp connected successfully!")
        else:
            self.logger.error("Warp connection failed!")
            
    def enable_warp_tunnel(self, enable_warp: bool):
        if not enable_warp:
            self.logger.info("Warp is disabled. Skipping Warp connection.")
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
            self.logger.info("Warp disconnected successfully!")

    def status(self):
        status_warp_result = subprocess.run(
            ["warp-cli", "status"],
            capture_output=True,
            text=True
        )
        if WarpStatus.CONNECTED.value in status_warp_result.stdout:
            return WarpStatus.CONNECTED
        return WarpStatus.DISCONNECTED
    
    def wait_for_connection(self, timeout=10):
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.status() == WarpStatus.CONNECTED:
                return True
            time.sleep(0.5)
        return False

    def unregister(self):
        unregister_warp_result = subprocess.run(
            ["warp-cli", "registration", "delete"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        if unregister_warp_result.returncode == 0:
            self.logger.info("Warp unregistered successfully!")