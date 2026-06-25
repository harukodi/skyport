import secrets, os
from nicegui import ui, app
from classes.LoginPage import LoginPage
from classes.DashboardPage import DashboardPage
from classes.Auth import Auth
from classes.AuthMiddleware import AuthMiddleware
from classes.NotFoundPage import NotFoundPage
from classes.DataStoreReader import DataStoreReader
from classes.BinaryProxer import BinaryProxer
from dotenv import load_dotenv


class AppBootstrap():
    def __init__(self, title: str):
        self.title = title
        self.production_mode = os.environ.get("PRODUCTION_MODE", "false").lower() == "true"
        self.app = app
        load_dotenv(override=True)

    def build_pages(self):
        LoginPage(on_login=Auth.verify_login, title=self.title, redirect_to="/dashboard").build()
        DashboardPage().build()
        NotFoundPage().build()

    def init_services(self):
        Auth.init()
        AuthMiddleware.register()
        BinaryProxer(self.app)
    
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
    app_ui = AppBootstrap(title="Skyport")

    if __name__ == "__main__":
        DataStoreReader().wait_for_data_store()
    
    app_ui.init_services()  
    app_ui.build_pages()
    app_ui.run()