import httpx, asyncio
from shared.logger import Logger
from enum import Enum

class Platform(str, Enum):
    WINDOWS_X64 = "v2rayN-windows-64.zip"
    WINDOWS_ARM64 = "v2rayN-windows-arm64.zip"
    ANDROID_UNIVERSAL = "universal.apk"
    LINUX_X64 = "v2rayN-linux-64.zip"
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
        Fetches the GitHub release download URL for the specified client platform.
        Args:
            platform: Target platform to fetch the binary URL for.
        Returns:
            Download URL string pointing to the latest GitHub release binary.
        Raises:
            ValueError: If the platform is not supported.
        """
        if platform in (Platform.WINDOWS_X64, Platform.WINDOWS_ARM64):
            return await self._fetch_windows_binary_url(platform)

        elif platform == Platform.ANDROID_UNIVERSAL:
            return await self._fetch_android_binary_url(platform)

        elif platform in (Platform.LINUX_X64, Platform.LINUX_ARM64):
            return await self._fetch_linux_binary_url(platform)

        else:
            raise ValueError("Unsupported platform")