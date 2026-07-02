from nicegui import ui, run
from classes.Auth import Auth
from datetime import datetime
from .ConfigLoader import ConfigLoader
from shared.warp_manager import WarpManager, WarpStatus

STARTED = datetime(2026, 5, 12, 0, 0, 0)
CARD_STYLE = "background-color: #252523; border-radius: 16px;"
BG_COLOR = "#1a1a18"
ORANGE = "#ff5722"
TEXT = "#f4f1ed"
MUTED = "#888780"
STATUS_ICONS = {
    WarpStatus.CONNECTED: ("link", "deep-orange"),
    WarpStatus.DISCONNECTED: ("link_off", MUTED),
}


class DashboardPage:
    def __init__(self):
        self.warp_manager = WarpManager()
        self.warp_error = False
    
    async def on_warp_toggle(self, e, warp_status, warp_switch, warp_spinner) -> None:
        warp_status.set_visibility(False)
        warp_spinner.set_visibility(True)
        warp_switch.disable()

        try:
            if e.value:
                await run.io_bound(self.warp_manager.connect)
                connected = await run.io_bound(self.warp_manager.wait_for_connection)

                if connected:
                    self.warp_error = False
                    warp_status.props(f"name={STATUS_ICONS[WarpStatus.CONNECTED][0]}").props("color=green")
                else:
                    self.warp_error = True
                    warp_switch.set_value(False)
                    warp_status.props(f"name={STATUS_ICONS[WarpStatus.DISCONNECTED][0]}").props("color=red")
                    ui.notify(
                        message="WARP connection failed. Server IP may be blocked or WARP may be unavailable!",
                        color="deep-orange",
                        type="warning",
                        icon="cloud_off"
                    )
            else:
                if not self.warp_error and self.warp_manager.status() == WarpStatus.CONNECTED:
                    await run.io_bound(self.warp_manager.disconnect)
                    warp_status.props(f"name={STATUS_ICONS[WarpStatus.DISCONNECTED][0]}").props("color=muted")
        finally:
            warp_switch.enable()
            warp_spinner.set_visibility(False)
            warp_status.set_visibility(True)

    def build(self) -> None:
        self.xray_client_qr_code_base64 = ConfigLoader.get_xray_qrcode()
        self.xray_client_vless_uri = ConfigLoader.get_xray_vless_uri()

        @ui.page("/dashboard")
        def dashboard():
            # Header and bg
            ui.query("body").style(f"background-color: {BG_COLOR};")
            with ui.column().classes("w-full max-w-sm mx-auto px-4 py-6 gap-3"):
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
                    ui.image(f"data:image/png;base64,{self.xray_client_qr_code_base64}").classes("w-48 mb-4").style(
                        f"border-radius: 12px; outline: 2px dashed {ORANGE}; outline-offset: 4px"
                    )
                    ui.button("COPY VLESS LINK", icon="content_copy", on_click=lambda: ui.clipboard.write(self.xray_client_vless_uri)).props("flat color=deep-orange")


                # WARP container
                with ui.card().classes("w-full h-[110px] overflow-hidden").style(CARD_STYLE):
                    with ui.row().classes("items-center gap-2"):
                        ui.icon("shield").style(f"color: {ORANGE}; font-size: 16px")
                        ui.label("WARP").style(
                            f"font-size: 12px; font-weight: 750; letter-spacing: 0.08em; color: {ORANGE}"
                        )

                    is_connected = self.warp_manager.status() == WarpStatus.CONNECTED
                    with ui.row().classes("w-full justify-between items-center"):
                        icon_name, icon_color = STATUS_ICONS[self.warp_manager.status()]
                        warp_status = ui.icon(icon_name).classes("px-[12px]").style(
                            f"font-size: 32px; color: {icon_color};"
                        )
                        warp_spinner = ui.spinner("dots", color="deep-orange").classes("w-14 h-4 px-[12px]")
                        warp_spinner.set_visibility(False)
                        warp_switch = ui.switch(value=is_connected).props("color=deep-orange")

                    warp_switch.on_value_change(
                        lambda e: self.on_warp_toggle(e, warp_status, warp_switch, warp_spinner)
                    )

                # Logout
                ui.button("Log out", icon="logout", on_click=lambda: Auth.logout()).classes(
                    "w-full rounded-xl"
                ).style(
                    f"background: none; border: 0.5px solid #444441; color: {ORANGE}; font-size: 14px"
                ).props("flat color=deep-orange")