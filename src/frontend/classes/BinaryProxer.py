import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from enum import Enum

class Platforms(str, Enum):
    android = "android"
    windows = "windows"
    linux = "linux"
    macos = "macos"

class BinaryProxer:
    PLATFORM_BINARIES = {
        Platforms.android: "https://github.com/2dust/v2rayNG/releases/latest/download/v2rayNG_2.2.5_universal.apk",
        Platforms.windows: "https://example.com/windows_binary.exe",
        Platforms.linux:   "https://example.com/linux_binary",
        Platforms.macos:   "https://example.com/macos_binary",
    }

    def __init__(self, app: FastAPI):
        self.app = app
        self.client = httpx.AsyncClient()
        self.api_route = "/client/dl/{platform}"
        self._register_routes()
        self._register_events()

    def _register_events(self):
        self.app.on_shutdown(self._on_shutdown)

    async def _on_shutdown(self):
        await self.client.aclose()
    
    def _register_routes(self):
        self.app.add_api_route(
            self.api_route,
            self.proxy_binary, 
            methods=["GET"]
        )
    
    async def proxy_binary(self, platform: Platforms):
        binary_url = self.PLATFORM_BINARIES.get(platform)
        if not binary_url:
            raise HTTPException(status_code=404, detail="Platform not supported")

        response = await self.client.send(
            self.client.build_request("GET", binary_url),
            stream=True,
            follow_redirects=True
        )

        if response.status_code != 200:
            await response.aclose()
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch binary, upstream returned an error")
        
        headers = {
            "Content-Encoding": "identity",
            "Cloudflare-CDN-Cache-Control": "no-store"
        }
        if content_length := response.headers.get("content-length"):
            headers["Content-Length"] = content_length
        if content_disposition := response.headers.get("content-disposition"):
            headers["Content-Disposition"] = content_disposition
        media_type = response.headers.get("content-type", "application/octet-stream")

        async def stream_chunks():
            async for chunk in response.aiter_bytes(chunk_size=128*1024):
                yield chunk
            await response.aclose()

        return StreamingResponse(
            stream_chunks(),
            media_type=media_type,
            headers=headers
        )