import secrets
from nicegui import ui, app
from classes.LoginPage import LoginPage
from classes.DashboardPage import DashboardPage
from classes.Auth import Auth
from classes.AuthMiddleware import AuthMiddleware
from classes.NotFoundPage import NotFoundPage
from dotenv import load_dotenv

app_title = "Skyport"
login_page = LoginPage(on_login=Auth.verify_login, title=app_title, redirect_to="/dashboard")
login_page.build()
dashboard_page = DashboardPage()
dashboard_page.build()
not_found_page = NotFoundPage()
not_found_page.build()

if __name__ in {"__main__", "__mp_main__"}:
    load_dotenv(override=True)
    Auth.init()
    AuthMiddleware.register()
    app.add_static_files("/assets", "assets")
    ui.run(storage_secret=secrets.token_hex(32), title=app_title)