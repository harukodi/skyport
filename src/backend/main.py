import atexit, signal, sys
from setup_cf_dns_record import setup_dns_record
from setup_xray_core import setup_xray_core
from classes.Services import Services
from classes.XrayConfig import XrayConfig
from classes.CaddyConfig import CaddyConfig
from classes.WarpHandler import WarpHandler
from classes.InfoPrinter import InfoPrinter
from pathlib import Path

service_manager = Services()
xray_config_manager = XrayConfig()
warp_handler = WarpHandler()
caddy_config_manager = CaddyConfig()
base_dir = Path(__file__).parent.resolve()

files_to_check = [
    base_dir / "xray_config" / "xray_config.json",
    base_dir / "xray_config" / "xray_client_qr_code.png",
    base_dir / "xray_config" / "xray_client_vless_link.json"
]

def initialize():
    setup_dns_record()
    setup_xray_core()
    warp_handler.enable_warp_tunnel()
    xray_config_manager.generate_xray_config()
    caddy_config_manager.generate_caddyfile()

def exit_function():
    def on_exit():
        warp_handler.disable_warp_tunnel()
        service_manager.stop_services()
    def handle_exit(signum, frame):
        sys.exit(0)
    atexit.register(on_exit)
    signal.signal(signal.SIGTERM, handle_exit)
    signal.signal(signal.SIGINT, handle_exit)
    signal.pause()

def main():
    if all(not file.exists() for file in files_to_check):
        initialize()
    else:
        setup_xray_core()
        warp_handler.enable_warp_tunnel()
    
    InfoPrinter.print_dashboard_url()
    InfoPrinter.print_vless_link()
    service_manager.start_services()
    exit_function()

if __name__ == "__main__":
    main()