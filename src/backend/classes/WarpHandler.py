from vars import enable_warp
from shared.warp import Warp

class WarpHandler:
    def __init__(self):
        self.enable_warp = True if enable_warp.lower() == "true" else False
        self.warp = Warp()
    
    def enable_warp_tunnel(self):
        self.warp.enable_warp_tunnel(self.enable_warp)

    def disable_warp_tunnel(self):
        self.warp.disconnect()
        self.warp.unregister()