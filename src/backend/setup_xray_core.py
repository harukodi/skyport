import json, platform, subprocess, urllib.error, sys
from os import path, remove
from urllib.request import urlretrieve
from urllib.request import urlopen
from zipfile import ZipFile
from vars import xray_version

arch_platform = platform.machine()
xray_core_path = "./xray_config/xray_core"

def chmod_xray_core():
    subprocess.run(["chmod", "+x", f"{xray_core_path}/xray"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

def unzip_xray_core():
    with ZipFile(f"{xray_core_path}/xray.zip", "r") as xray_zip_file:
        xray_zip_file.extractall(path=xray_core_path)
    for file in [f"{xray_core_path}/xray.zip", f"{xray_core_path}/README.md"]: remove(file)

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
    if arch_platform in ["AMD64", "x86_64"]:
        xray_base_url = f"https://github.com/XTLS/Xray-core/releases/download/v{version}/Xray-linux-64.zip"
    if arch_platform in ["aarch64"]:
        xray_base_url = f"https://github.com/XTLS/Xray-core/releases/download/v{version}/Xray-linux-arm64-v8a.zip"
    try:
        urlretrieve(xray_base_url, f"{xray_core_path}/xray.zip")
        unzip_xray_core()

        if arch_platform in ["AMD64", "x86_64"]:
            print(f"Xray-core: {version} x86_64")
        if arch_platform in ["aarch64"]:
            print(f"Xray-core: {version} aarch64")
    except Exception as e:
        print(f"Xray-binary: failed to download, error: {e.reason}")
        if not path.exists(f"{xray_core_path}/xray"):
            print("Xray binary not found. Try restarting the container!")
            sys.exit(1)
        else:
            print("Falling back to the previously installed binary.")

def setup_xray_core():
    if xray_version.lower() != "latest":
        download_xray_binary(xray_version)
    else:
        download_xray_binary(fetch_latest_xray_version_tag())
    chmod_xray_core()