import httpx
from nicegui import app
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from .ClientBinariesManager import ClientBinariesManager, Platform

class BinaryProxer:
    def __init__(self):
        self.client = httpx.AsyncClient()
        self.client_binaries_manager = ClientBinariesManager()
        self.api_route = "/client/dl/{platform}"
        self._register_routes()
        self._register_events()
        self.chunk_size = 512 * 1024

    def _register_events(self):
        app.on_shutdown(self._on_shutdown)

    async def _on_shutdown(self):
        await self.client.aclose()
    
    def _register_routes(self):
        app.add_api_route(
            self.api_route,
            self.proxy_binary, 
            methods=["GET"]
        )
    
    async def proxy_binary(self, platform: str) -> StreamingResponse:
        """
        Streams a client binary from GitHub to the user without saving to disk.
        This endpoint is unauthenticated and accessible via the frontend login page.
        Args:
            platform: Platform identifier, e.g. 'windows_x86' or 'android_universal'.
        Returns:
            StreamingResponse with the binary as application/octet-stream.
        Raises:
            HTTPException: 404 if the platform is not recognized.
        """
        platform_enum = Platform[platform.upper()]
        binary_url = await self.client_binaries_manager.get_client_binary_url(platform_enum)
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
            async for chunk in response.aiter_bytes(chunk_size=self.chunk_size):
                yield chunk
            await response.aclose()

        return StreamingResponse(
            stream_chunks(),
            media_type=media_type,
            headers=headers
        )