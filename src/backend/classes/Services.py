import subprocess, json, tempfile
from pathlib import Path
from vars import enable_caddy_log, enable_warp

class Services:
    def __init__(self):
        self.base_dir = Path(".").parent.resolve()
        self.xray_process = None
        self.caddy_process = None
        self.xray_binary_path = self.base_dir / "xray_config" / "xray_core" / "xray"
        self.xray_config_path = self.base_dir / "xray_config" / "xray_config.json"
        self.xray_socks_outbound_config_path = self.base_dir / "templates" / "xray_socks_template.json"
        self.caddy_config_path = self.base_dir / "caddy_config" / "Caddyfile"
        self.enable_caddy_log = enable_caddy_log

    def _start_caddy(self):
        if self.enable_caddy_log.lower() == "true":
            self.caddy_process = subprocess.Popen(
                ["caddy", "run", "--config", self.caddy_config_path]
            )
        else:
            self.caddy_process = subprocess.Popen(
                ["caddy", "run", "--config", self.caddy_config_path],
                stderr=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL
            )

    def _read_template(self, template_file):
        with open(template_file, "r") as template_file:
            template = json.load(template_file)
        return template

    def _start_xray(self):
        if enable_warp.lower() == "true":
            xray_config = self._read_template(self.xray_config_path)
            socks_config = self._read_template(self.xray_socks_outbound_config_path)
            xray_config["outbounds"].insert(0, socks_config)
            
            with tempfile.NamedTemporaryFile("w+", prefix="xray_config", suffix=".json" , delete=False) as xray_config_temp:
                json.dump(xray_config, xray_config_temp, indent=4)
                xray_config_temp.flush()
            
                self.xray_process = subprocess.Popen(
                    [self.xray_binary_path, "run", "-c", xray_config_temp.name]
                )
        else:
            self.xray_process = subprocess.Popen(
                [self.xray_binary_path, "run", "-c", self.xray_config_path]
            )

    def start_services(self):
        self._start_xray()
        self._start_caddy()

    def stop_services(self):
        self.caddy_process.kill()
        self.xray_process.kill()