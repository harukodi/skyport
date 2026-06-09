import atexit, signal, sys
from os import path
from setup_cf_dns_record import setup_dns_record
from setup_xray_core import setup_xray_core
from generate_caddy_config import generate_caddy_config
from classes.Services import Services
from classes.XrayConfig import XrayConfig
from classes.Warp import Warp

service_manager = Services()
xray_config_manager = XrayConfig()
warp_manager = Warp()
files_to_check = [
    "./xray_config/xray_config.json",
    "./xray_config/xray_client_qr_code.png",
    "./xray_config/xray_client_vless_link.json"
]

def initialize():
    setup_dns_record()
    setup_xray_core()
    warp_manager.enable_warp_tunnel()
    xray_config_manager.generate_xray_config()
    xray_config_manager.generate_xray_qr_code_and_vless_link()
    generate_caddy_config()

def exit_function():
    def on_exit():
        warp_manager.disconnect()
        warp_manager.unregister()
        service_manager.stop_services()
    def handle_exit(signum, frame):
        sys.exit(0)
    atexit.register(on_exit)
    signal.signal(signal.SIGTERM, handle_exit)
    signal.signal(signal.SIGINT, handle_exit)
    signal.pause()

def main():
    if all(not path.exists(file) for file in files_to_check):
        initialize()
    else:
        setup_xray_core()
        warp_manager.enable_warp_tunnel()
    
    service_manager.start_services()
    exit_function()

if __name__ == "__main__":
    main()