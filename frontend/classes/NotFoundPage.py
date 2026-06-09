from nicegui import ui, app
from fastapi import Request
from fastapi.responses import RedirectResponse
from classes.Auth import Auth

class NotFoundPage:
    def build(self) -> None:

        @app.exception_handler(404)
        async def not_found_handler(request: Request, exc):
            return RedirectResponse("/404")

        @ui.page("/404")
        def not_found():
            with ui.column().classes("absolute-center items-center gap-4"):
                ui.label("404").classes("text-8xl font-bold")
                ui.label("Page not found!")
                ui.button("Go back", on_click=lambda: ui.navigate.to("/dashboard"))