import secrets
from nicegui import ui, app
from classes.LoginPage import LoginPage
from classes.DashboardPage import DashboardPage
from classes.Auth import Auth
from classes.AuthMiddleware import AuthMiddleware
from classes.NotFoundPage import NotFoundPage
from classes.XrayConfigLoader import XrayConfigLoader
from dotenv import load_dotenv

class AppBootstrap():
    def __init__(self, title: str):
        self.title = title
    
    def build_pages(self):
        LoginPage(on_login=Auth.verify_login, title=self.title, redirect_to="/dashboard").build()
        DashboardPage().build()
        NotFoundPage().build()

    def init_services(self):
        XrayConfigLoader.init()
        Auth.init()
        AuthMiddleware.register()
        app.add_static_files("/assets", "assets")
    
    def run(self):
        ui.run(
            storage_secret=secrets.token_hex(32),
            title=self.title
        )

if __name__ in {"__main__", "__mp_main__"}:
    load_dotenv(override=True)
    app_ui = AppBootstrap(title="Skyport")

    app_ui.init_services()
    app_ui.build_pages()
    app_ui.run()