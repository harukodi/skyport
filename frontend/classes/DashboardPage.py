from nicegui import ui
from classes.Auth import Auth
from datetime import datetime
from pathlib import Path

STARTED = datetime(2026, 5, 12, 0, 0, 0)
CARD_STYLE = "background-color: #252523; border-radius: 16px;"
BG_COLOR = "#1a1a18"
ORANGE = "#ff5722"
TEXT = "#f4f1ed"
MUTED = "#888780"

class DashboardPage:
    def build(self) -> None:

        @ui.page("/dashboard")
        def dashboard():
            ui.query("body").style(f"background-color: {BG_COLOR};")

            with ui.column().classes("w-full max-w-sm mx-auto px-4 py-6 gap-3"):

                # Header
                with ui.column().classes("gap-0"):
                    ui.label("Dashboard").style(f"font-size: 26px; font-weight: 750; color: {ORANGE}")
                    ui.label(datetime.now().strftime("%a, %b %d")).style(
                        f"font-size: 13px; color: {MUTED}; font-family: monospace"
                    )

                # QR Connect card and link
                with ui.card().classes("w-full items-center").style(CARD_STYLE):
                    with ui.row().classes("items-center gap-2 self-start mb-4"):
                        ui.icon("wifi").style(f"color: {ORANGE}; font-size: 16px")
                        ui.label("QR CODE").style(
                            f"font-size: 12px; font-weight: 750; letter-spacing: 0.08em; color: {ORANGE}"
                        )
                    ui.image(self.qr_code_path).classes("w-48 mb-4").style(
                        f"border-radius: 12px; outline: 2px dashed {ORANGE}; outline-offset: 4px"
                    )
                    ui.button("COPY VLESS LINK", icon="content_copy", on_click=lambda: ui.clipboard.write(self.vless_link)).props("flat color=deep-orange")


                # WARP card
                with ui.card().classes("w-full").style(CARD_STYLE):
                    with ui.row().classes("items-center gap-2 mb-4"):
                        ui.icon("shield").style(f"color: {ORANGE}; font-size: 16px")
                        ui.label("WARP").style(
                            f"font-size: 12px; font-weight: 750; letter-spacing: 0.08em; color: {ORANGE}"
                        )

                    with ui.row().classes("w-full items-center justify-between"):
                        warp_status = ui.label("Connected").style(
                            f"font-size: 18px; font-weight: 500; color: {TEXT}"
                        )
                        warp_switch = ui.switch("", value=False).props("color=deep-orange")

                    def on_warp_toggle(e):
                        if e.value:
                            warp_status.set_text("Connected")
                            warp_status.style(f"font-size: 18px; font-weight: 500; color: {TEXT}")
                        else:
                            warp_status.set_text("Disconnected")
                            warp_status.style(f"font-size: 18px; font-weight: 500; color: {MUTED}")

                    warp_switch.on_value_change(on_warp_toggle)

                # Logout
                ui.button("Log out", icon="logout", on_click=lambda: Auth.logout()).classes(
                    "w-full rounded-xl"
                ).style(
                    f"background: none; border: 0.5px solid #444441; color: {ORANGE}; font-size: 14px"
                ).props("flat color=deep-orange")