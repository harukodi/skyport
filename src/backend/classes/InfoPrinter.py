import os
from .DataStore import DataStore
from vars import domain_name

class InfoPrinter:
    data_store = DataStore()
    enable_skyport_ui = os.environ.get("SKYPORT_UI", "false").lower() == "true"
    
    @classmethod
    def print_vless_link(cls):
        vless_link = cls.data_store.get("vless_uri")
        print("=" * 21)
        print("VLESS CONNECTION LINK")
        print("=" * 21)
        print(f"{vless_link}\n")

    @classmethod
    def print_dashboard_url(cls):
        if cls.enable_skyport_ui:
            frontend_path = cls.data_store.get("frontend_path")
            dashboard_url = f"https://{domain_name}/{frontend_path}/"
            print("=" * 13)
            print("DASHBOARD URL")
            print("=" * 13)
            print(f"{dashboard_url}\n")