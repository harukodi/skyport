import secrets, os
from nicegui import ui, app
from classes.LoginPage import LoginPage
from classes.DashboardPage import DashboardPage
from classes.Auth import Auth
from classes.AuthMiddleware import AuthMiddleware
from classes.NotFoundPage import NotFoundPage
from classes.XrayConfigLoader import XrayConfigLoader
from dotenv import load_dotenv
from pathlib import Path


class AppBootstrap():
    def __init__(self, title: str):
        self.title = title
        self.production_mode = os.environ.get("PRODUCTION_MODE", "false").lower() == "true"
        self.assets_dir = Path(__file__).parent.resolve() / "assets"

    def build_pages(self):
        LoginPage(on_login=Auth.verify_login, title=self.title, redirect_to="/dashboard").build()
        DashboardPage().build()
        NotFoundPage().build()

    def init_services(self):
        Auth.init()
        AuthMiddleware.register()
        app.add_static_files("/assets", self.assets_dir)
    
    def run(self):
        if self.production_mode:
            os.environ["NODE_OPTIONS"] = "--no-deprecation"
            ui.run(
                host="0.0.0.0",
                storage_secret=secrets.token_hex(32),
                title=self.title,
                reload=False,
                show_welcome_message=False,
            )
        else:
            ui.run(
                storage_secret=secrets.token_hex(32),
                title=self.title,
                reload=True
            )

if __name__ in {"__main__", "__mp_main__"}:
    load_dotenv(override=True)
    app_ui = AppBootstrap(title="Skyport")
    
    if __name__ == "__main__":
        XrayConfigLoader.init()
        
    app_ui.init_services()
    app_ui.build_pages()
    app_ui.run()