from nicegui import ui, app
from classes.Auth import Auth
from .ClientBinariesManager import Platform

BG_COLOR = "#1a1a18"

class LoginPage:
    def __init__(self, on_login: callable, title: str, redirect_to: str):
        self.on_login = on_login
        self.title = title
        self.redirect_to = redirect_to

    def _build_download_section(self) -> None:
        # Removes the box shadow from the dropdown menu
        ui.add_css('''
            @layer overrides {
                .q-menu--dark {
                    box-shadow: none !important;
                    border-radius: 0.5rem !important;
                    margin-top: 4px !important;
                }
            }
        ''')
        with ui.column().classes("items-center w-68"):
            with ui.dropdown_button("Get clients", icon="devices").classes("w-68 rounded-lg py-2").props("flat color=deep-orange dark dropdown-icon=unfold_more no-icon-animation").style("border: 0.5px solid #D85A30"):
                for platform in Platform:
                    ui.item(
                        platform.name.replace("_", " ").lower().capitalize(),
                        on_click=lambda p=platform: ui.navigate.to(f"/client/dl/{p.name.lower()}", new_tab=False)
                    ).style("background-color: #252523; color: #D85A30")

    def build(self) -> None:
        @ui.page("/")
        def login_view():
            if Auth.redirect_if_authenticated("/dashboard"):
                return
            ui.dark_mode().enable()
            ui.query("body").style(f"background-color: {BG_COLOR}")

            with ui.column().classes("absolute-center items-center gap-4"):
                ui.label(self.title).style("font-size: 2.8rem; font-weight: 500; color: #D85A30; margin-bottom: 16px; margin-top: -80px")

                with ui.card().classes("items-center gap-4").style("background-color: #252523; border-radius: 16px; padding: 32px; box-shadow: none"):
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

                    ui.button("Sign in", icon="login", on_click=handle_login).classes("w-68 rounded-lg py-2").props(
                        "flat color=deep-orange"
                    ).style("border: 0.5px solid #D85A30")

                    username.on("keydown.enter", handle_login)
                    password.on("keydown.enter", handle_login)
                    
                    self._build_download_section()