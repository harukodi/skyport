import shutil, json
from pathlib import Path
from shared.logger import Logger
from time import sleep

class XrayConfigLoader:
    base_dir = Path(__file__).parent.parent.parent.resolve()
    dst_dir = Path(__file__).parent.parent.resolve() / "assets" / "xray_data"
    xray_qr_code_file = base_dir / "backend" / "xray_config" / "xray_client_qr_code.png"
    xray_vless_link_file = base_dir / "backend" / "xray_config" / "xray_client_vless_link.json"
    xray_config_loader_logger = Logger("XrayConfigLoader")

    @classmethod
    def init(cls) -> None:
        cls.dst_dir.mkdir(parents=True, exist_ok=True)
        xray_config_files = (
            (cls.xray_qr_code_file, "xray_client_qr_code.png"),
            (cls.xray_vless_link_file, "xray_client_vless_link.json")
        )

        for src, file_name in xray_config_files:
            for attempt in range(10):
                if src.exists():
                    shutil.copy2(src, cls.dst_dir / file_name)
                    cls.xray_config_loader_logger.info(f"Copied {file_name} to {cls.dst_dir / file_name}")
                    break
                cls.xray_config_loader_logger.warning(f"{file_name} not found. Attempt {attempt + 1}/10. Retrying in 5 seconds...")
                sleep(5)
            else:
                raise FileNotFoundError(f"Could not find {src} after 10 attempts. Unable to start the frontend application.")

    @classmethod
    def get_xray_qrcode_path(cls) -> str:
        return Path(cls.dst_dir) / "xray_client_qr_code.png"
    
    @classmethod
    def get_xray_vless_link(cls):
        with open(cls.dst_dir / "xray_client_vless_link.json", "r") as file:
            data = json.load(file)
        return data["xray_client_vless_link"]