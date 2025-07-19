from ignis import utils, widgets
from ignis.css_manager import CssManager
from ignis.services.bluetooth import BluetoothService
from ignis.services.network import NetworkService
from user_options import user_options

bluetooth = BluetoothService.get_default()
network = NetworkService.get_default()

css_manager = CssManager().get_default()

class QSButton(widgets.Button):
    def __init__(self, icon_name: str, label_top: str, label_bottom: str):
        super().__init__()
        self.css_classes = ["control-center-qs-button"]
        self.child = widgets.Box(
            hexpand = True,
            child = [
                widgets.Icon(
                    css_classes = ["control-center-qs-icon"],
                    icon_name = icon_name,
                    pixel_size = 20,
                ),
                widgets.Box(
                    hexpand = True,
                    vertical = True,
                    child = [
                        widgets.Label(
                            label = label_top,
                        ),
                        widgets.Label(
                            css_classes = ["control-center-qs-label-bottom"],
                            label = label_bottom,
                        ),
                    ],
                ),
            ],
        )


class Wifi(QSButton):
    def __init__(self):
        super().__init__(
            icon_name = network.wifi.bind("icon_name"),
            label_top = "Wifi",
            label_bottom = network.wifi.bind_many(["enabled", "is_connected"],
                lambda enabled, is_connected: "off" if not enabled else ("disconnected" if not is_connected else network.wifi.devices[0].bind("ap",
                    lambda ap: ap.bind("ssid", lambda ssid: ssid if len(ssid) <= 23 else ssid[:20] + "...")
                )),
            ),
        )
        if network.wifi.enabled:
            self.add_css_class("enabled")
        network.wifi.connect("notify::enabled", lambda wifi, enabled: self.__update_css())

        self.on_click = lambda _: self.__on_click() 

    def __on_click(self):
        network.wifi.enabled = not network.wifi.enabled

    def __update_css(self):
        if network.wifi.enabled:
            self.add_css_class("enabled")
        else:
            self.remove_css_class("enabled")

class Bluetooth(QSButton):
    def __init__(self):
        super().__init__(
            icon_name = bluetooth.bind("powered", lambda powered: "bluetooth-active-symbolic" if powered else "bluetooth-disabled-symbolic"),
            label_top = "Bluetooth",
            label_bottom = bluetooth.bind_many(["state", "connected_devices"], lambda state, connected_devices:
                state if (state != "on" or len(connected_devices) == 0) else (bluetooth.connected_devices[0].alias if len(connected_devices) == 1 else f"{len(connected_devices)} devices connected"),
            ),
        )
        if bluetooth.powered:
            self.add_css_class("enabled")
        bluetooth.connect("notify::powered", lambda bluetooth, powered: self.__update_css())
        self.on_click = lambda _: self.__on_click()
    
    def __on_click(self):
        bluetooth.powered = not bluetooth.powered

    def __update_css(self):
        if bluetooth.powered:
            self.add_css_class("enabled")
        else:
            self.remove_css_class("enabled")

class DarkMode(QSButton):
    def __init__(self):
        super().__init__(
            icon_name = "weather-clear-night",
            label_top = "Dark mode",
            label_bottom = user_options.appearance.bind("dark_mode", lambda dark_mode: "on" if dark_mode else "off"),
        )
        if user_options.appearance.dark_mode:
            self.add_css_class("enabled")
        self.on_click = lambda _: self.__on_click()

    def __on_click(self):
        if user_options.appearance.dark_mode:
            user_options.appearance.dark_mode = False
            self.remove_css_class("enabled")
            utils.exec_sh(f"swww img {user_options.appearance.wallpaper_light} --transition-type wave --transition-fps 120 --transition-duration 1")
            utils.exec_sh("gsettings set org.gnome.desktop.interface color-scheme prefer-light")
        else:
            user_options.appearance.dark_mode = True
            self.add_css_class("enabled")
            utils.exec_sh(f"swww img {user_options.appearance.wallpaper_dark} --transition-type wave --transition-fps 120 --transition-duration 1")
            utils.exec_sh("gsettings set org.gnome.desktop.interface color-scheme prefer-dark")
        css_manager.reload_all_css()

class DoNotDisturb(QSButton):
    def __init__(self):
        super().__init__(
            icon_name = user_options.bind("do_not_disturb", lambda dnd: "user-available-symbolic" if dnd else "user-offline-symbolic"),
            label_top = "Do not disturb",
            label_bottom = user_options.bind("do_not_disturb", lambda dnd: "on" if dnd else "off"),
        )
        if user_options.do_not_disturb:
            self.add_css_class("enabled")
        self.on_click = lambda _: self.__on_click()

    def __on_click(self):
        if user_options.do_not_disturb:
            user_options.do_not_disturb = False
            self.remove_css_class("enabled")
        else:
            user_options.do_not_disturb = True
            self.add_css_class("enabled")

class QuickSettings(widgets.Box):
    def __init__(self):
        super().__init__()
        self.css_classes = ["control-center-qs-container"]
        self.hexpand = True
        self.child = [
            widgets.Box(
                vertical = True,
                child = [
                    Wifi(),
                    DarkMode(),
                ],
            ),
            widgets.Box(
                vertical = True,
                child = [
                    Bluetooth(),
                    DoNotDisturb(),
                ],
            ),
        ]
