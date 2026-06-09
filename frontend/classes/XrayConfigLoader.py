import shutil, json
from pathlib import Path

class XrayConfigLoader:
    base_dir = Path(__file__).parent.parent.parent
    dst_dir = Path(__file__).parent.parent / "assets" / "xray_data"
    xray_qr_code_file = base_dir / "app" / "xray_config" / "xray_client_qr_code.png"
    xray_vless_link_file = base_dir / "app" / "xray_config" / "xray_client_vless_link.json"

    @classmethod
    def init(cls) -> None:
        cls.dst_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(
            cls.xray_qr_code_file,
            cls.dst_dir / "xray_client_qr_code.png"
        )
        shutil.copy2(
            cls.xray_vless_link_file,
            cls.dst_dir / "xray_client_vless_link.json"
        )

    @classmethod
    def get_xray_qrcode_path(cls) -> str:
        return Path(cls.dst_dir) / "xray_client_qr_code.png"
    
    @classmethod
    def get_xray_vless_link(cls):
        with open(cls.dst_dir / "xray_client_vless_link.json", "r") as file:
            data = json.load(file)
        return data["xray_client_vless_link"]