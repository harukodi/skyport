from .DataStoreReader import DataStoreReader

class ConfigLoader:
    @classmethod
    def get_xray_qrcode(cls) -> str:
        return DataStoreReader().get("qr_code_base64")
    
    @classmethod
    def get_xray_vless_uri(cls):
        return DataStoreReader().get("vless_uri")
    
    @classmethod
    def get_frontend_path(cls):
        return DataStoreReader().get("frontend_path")