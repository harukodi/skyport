from nicegui import ui, app
from classes.Auth import Auth

BG_COLOR = "#1a1a18"

class LoginPage:
    def __init__(self, on_login: callable, title: str, redirect_to: str):
        self.on_login = on_login
        self.title = title
        self.redirect_to = redirect_to

    def build(self) -> None:

        @ui.page("/")
        def login_view():
            if Auth.redirect_if_authenticated("/dashboard"):
                return

            ui.query("body").style(f"background-color: {BG_COLOR}")

            with ui.column().classes("absolute-center items-center gap-4"):
                ui.label(self.title).style("font-size: 2rem; font-weight: 500; color: #D85A30; margin-bottom: 16px; margin-top: -80px")

                with ui.card().classes("items-center gap-4").style("background-color: #252523; border-radius: 16px; padding: 32px"):
                    username = ui.input(label="Username").classes("w-68").props(
                        'dark color=deep-orange flat dense'
                    )
                    password = ui.input(label="Password", password=True, password_toggle_button=False).classes("w-68").props(
                        'dark color=deep-orange flat dense'
                    )

                    error_label = ui.label("").classes("text-sm").style("color: #D85A30")

                    def handle_login():
                        result = self.on_login(username.value, password.value)
                        if result:
                            Auth.login(redirect_to=self.redirect_to)
                        else:
                            error_label.set_text("Wrong username or password")

                    ui.button("Log in", icon="login", on_click=handle_login).classes("w-68 rounded-lg py-2").props(
                        "flat color=deep-orange"
                    ).style("border: 0.5px solid #D85A30")

                    username.on("keydown.enter", handle_login)
                    password.on("keydown.enter", handle_login)