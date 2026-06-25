import httpx, asyncio
from shared.logger import Logger
from enum import Enum

class Platform(str, Enum):
    WINDOWS_X86 = "v2rayN-windows-64.zip"
    WINDOWS_ARM64 = "v2rayN-windows-arm64.zip"
    ANDROID_UNIVERSAL = "universal.apk"
    LINUX_X86 = "v2rayN-linux-64.zip"
    LINUX_ARM64 = "v2rayN-linux-arm64.zip"

class ClientBinariesManager:
    V2RAYN_REPO = ("2dust", "v2rayn")
    V2RAYNG_REPO = ("2dust", "v2rayNG")

    def __init__(self):
        self.base_url = "https://api.github.com"
        self.logger = Logger("ClientBinariesManager")
        self.client = httpx.AsyncClient(
            base_url=self.base_url, timeout=10.0,
        )
    
    async def _get_latest_assets(self, owner: str, repo: str) -> list:
        response = await self.client.get(f"/repos/{owner}/{repo}/releases/latest")
        response.raise_for_status()
        return response.json()["assets"]
    
    async def _fetch_windows_binary_url(self, platform: Platform) -> str:
        owner, repo = self.V2RAYN_REPO
        assets = await self._get_latest_assets(owner, repo)
        asset = next(
            asset for asset in assets 
            if asset["name"] == platform.value
        )
        return asset["browser_download_url"]
    
    async def _fetch_android_binary_url(self, platform: Platform) -> str:
        owner, repo = self.V2RAYNG_REPO
        assets = await self._get_latest_assets(owner, repo)
        asset = next(
            asset for asset in assets
            if platform.value in asset["name"] and "fdroid" not in asset["name"]
        )
        return asset["browser_download_url"]

    async def _fetch_linux_binary_url(self, platform: Platform) -> str:
        owner, repo = self.V2RAYN_REPO
        assets = await self._get_latest_assets(owner, repo)
        asset = next(
            asset for asset in assets
            if asset["name"] == platform.value
        )
        return asset["browser_download_url"]
    
    async def get_client_binary_url(self, platform: Platform) -> str:
        """
        Gets the download URL for the specified architecture.
        """
        if platform in (Platform.WINDOWS_X86, Platform.WINDOWS_ARM64):
            platform = Platform(platform.value)
            return await self._fetch_windows_binary_url(platform)
        
        elif platform == Platform.ANDROID_UNIVERSAL:
            return await self._fetch_android_binary_url(platform)
        
        elif platform in (Platform.LINUX_X86, Platform.LINUX_ARM64):
            platform = Platform(platform.value)
            return await self._fetch_linux_binary_url(platform)
        
        else:
            raise ValueError("Unsupported platform")
        

async def main():
    manager = ClientBinariesManager()
    platforms = [
        Platform.WINDOWS_X86,
        Platform.WINDOWS_ARM64,
        Platform.ANDROID_UNIVERSAL,
        Platform.LINUX_X86,
        Platform.LINUX_ARM64
    ]
    for platform in platforms:
        url = await manager.get_client_binary_url(platform)
        print(f"{platform.value}: {url}")

asyncio.run(main())