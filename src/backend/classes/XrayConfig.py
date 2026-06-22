import subprocess, segno, shelve, io, base64
from vars import xray_uuid, xray_path, xray_encryption_key, xray_decryption_key, domain_name, port
from string import Template
from pathlib import Path
from urllib.parse import quote
from .DataStore import DataStore

class XrayConfig:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent.resolve()
        self.xray_config_template = self.base_dir / "templates" / "xray_config_template.json"
        self.xray_config_file = self.base_dir / "xray_config" / "xray_config.json"
        self.xray_binary_path = self.base_dir / "xray_config" / "xray_core"
        self.data_store = DataStore()
        self.xray_uuid = xray_uuid
        self.xray_path = xray_path
        self.xray_encryption_key = xray_encryption_key
        self.xray_decryption_key = xray_decryption_key
        self.domain_name = domain_name
        self.port = port
    
    def _generate_vlessenc_keys(self):
        if self.xray_encryption_key != None and self.xray_decryption_key != None:
            return

        xray_vlessenc_result = subprocess.run(
            f"{self.xray_binary_path}/xray vlessenc | awk 'NF' | awk 'NF==2' | head -n 2",
            capture_output=True,
            shell=True,
            text=True
        )
        filtered_xray_vlessenc_result = xray_vlessenc_result.stdout.strip().split('\n')
        
        for line in filtered_xray_vlessenc_result:
            filtered_lines = line.replace('"', '').replace(' ', '')
            key, value = filtered_lines.split(":")
            if key == "encryption" and self.xray_encryption_key is None:
                self.xray_encryption_key = value
            if key == "decryption" and self.xray_decryption_key is None:
                self.xray_decryption_key = value

    def _generate_xray_qr_code_and_vless_link(self):
        encoded_remark = quote(self.domain_name, safe="")
        vless_uri = f"vless://{self.xray_uuid}@{self.domain_name}:{self.port}?encryption={self.xray_encryption_key}&flow=xtls-rprx-vision&security=tls&sni={self.domain_name}&alpn=h3%2Ch2%2Chttp%2F1.1&type=xhttp&host={self.domain_name}&path={self.xray_path}&mode=auto#{encoded_remark}"
        
        buffer = io.BytesIO()
        qr_code = segno.make_qr(vless_uri)
        qr_code.save(buffer, kind="png", border=3, scale=10)
        qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        self.data_store.insert("vless_uri", vless_uri)
        self.data_store.insert("qr_code_base64", qr_code_base64)

    def generate_xray_config(self):
        self._generate_vlessenc_keys()
        self._generate_xray_qr_code_and_vless_link()
        xray_config_substitute_values = {
            "xray_uuid": self.xray_uuid,
            "xray_path": self.xray_path,
            "xray_decryption_key": self.xray_decryption_key
        }
    
        with open(self.xray_config_template, 'r') as file:
            xray_config = file.read()
            xray_config_filled = Template(xray_config).substitute(xray_config_substitute_values)
    
        with open(self.xray_config_file, 'w') as file:
            file.write(xray_config_filled)