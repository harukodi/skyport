import shutil, json
from pathlib import Path

class XrayConfigLoader:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.xray_qr_code_file = self.base_dir / "app" / "xray_config" / "xray_client_qr_code.png"
        self.xray_vless_link_file = self.base_dir / "app" / "xray_config" / "xray_client_vless_link.json"
        self.dst_dir = Path(__file__).parent / "assets" / "xray_data"
        self.dst_dir.mkdir(Parents=True, exist_ok=True)
        self.copy_xray_qrcode_and_vless_link()
    
    def copy_xray_qrcode_and_vless_link(self) -> None:
        shutil.copy2(
            self.xray_qr_code_file,
            self.dst_dir / "xray_client_qr_code.png"
        )
        shutil.copy2(
            self.xray_vless_link_file,
            self.dst_dir / "xray_client_vless_link.json"
        )

    @property
    def xray_qrcode_path(self) -> str:
        return Path(self.dst_dir) / "xray_client_qr_code.png"
    
    @property
    def xray_vless_link(self):
        with open(f"{self.dst_dir}/xray_client_vless_link.json", "r") as file:
            data = json.load(file)
        return data["xray_client_vless_link"]