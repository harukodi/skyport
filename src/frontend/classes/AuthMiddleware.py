from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from nicegui import app
from classes.Auth import Auth

unrestricted_paths = {"/"}

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        requested_path = request.url.path
        if not requested_path.startswith("/_nicegui") and requested_path not in unrestricted_paths:
            if not Auth.is_authenticated():
                return RedirectResponse("/")
        return await call_next(request)

    @classmethod
    def register(cls) -> None:
        app.add_middleware(cls)