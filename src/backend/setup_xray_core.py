import json, platform, subprocess, urllib.error, sys
from os import path, remove
from urllib.request import urlretrieve
from urllib.request import urlopen
from zipfile import ZipFile
from vars import xray_version
from pathlib import Path

arch_platform = platform.machine()
xray_core_path = Path(__file__).parent / "xray_config/xray_core"
ARCH_MAP = {
    "x86_64": ("Xray-linux-64.zip", "x86_64"),
    "AMD64":  ("Xray-linux-64.zip", "x86_64"),
    "aarch64": ("Xray-linux-arm64-v8a.zip", "aarch64"),
}

def chmod_xray_core():
    subprocess.run(["chmod", "+x", xray_core_path / "xray"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

def unzip_xray_core():
    with ZipFile(xray_core_path / "xray.zip", "r") as xray_zip_file:
        xray_zip_file.extractall(path=xray_core_path)
    (xray_core_path / "xray.zip").unlink()
    (xray_core_path / "README.md").unlink(missing_ok=True)

def fetch_latest_xray_version_tag():
    xray_releases_url = "https://api.github.com/repos/XTLS/Xray-core/releases"
    response = urlopen(xray_releases_url)
    json_data = json.loads(response.read().decode('utf-8'))
    for item in json_data:
        if not item['prerelease']:
            xray_tag = f"{item['tag_name']}"
            xray_tag_formatted = xray_tag.replace("v", "")
            return xray_tag_formatted

def download_xray_binary(version):
    if arch_platform not in ARCH_MAP:
        print(f"Unsupported architecture: {arch_platform}")
        sys.exit(1)

    zip_name, arch_label = ARCH_MAP[arch_platform]
    xray_base_url = f"https://github.com/XTLS/Xray-core/releases/download/v{version}/{zip_name}"
    xray_binary = xray_core_path / "xray"

    try:
        urlretrieve(xray_base_url, xray_core_path / "xray.zip")
        print(f"Xray-core: {version} {arch_label}")
    except Exception as e:
        print(f"Xray-binary: failed to download, error: {e}")
        if xray_binary.exists():
            print("Falling back to the previously installed binary.")
            return
        else:
            print("Xray binary not found. Try restarting the container!")
            sys.exit(1)

    unzip_xray_core()

def setup_xray_core():
    if xray_version.lower() != "latest":
        download_xray_binary(xray_version)
    else:
        download_xray_binary(fetch_latest_xray_version_tag())
    chmod_xray_core()