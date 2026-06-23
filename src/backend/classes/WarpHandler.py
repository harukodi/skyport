from vars import enable_warp
from shared.warp_manager import WarpManager

class WarpHandler:
    def __init__(self):
        self.enable_warp = True if enable_warp.lower() == "true" else False
        self.warp_manager = WarpManager()
    
    def enable_warp_tunnel(self):
        self.warp_manager.enable_warp_tunnel(self.enable_warp)

    def disable_warp_tunnel(self):
        self.warp_manager.disconnect()
        self.warp_manager.unregister()