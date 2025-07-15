from ignis import widgets
from ignis.css_manager import CssManager
from ignis import utils
from user_options import user_options

css_manager = CssManager().get_default()

class DarkModeToggle(widgets.Button):
    def __init__(self):
        super().__init__()
        self.css_classes = ["bar-dark-mode-button"]
        self.child = widgets.Icon(icon_name = "weather-clear-night")
        self.on_click = lambda _: self.__on_click()

    def __on_click(self):
        if user_options.appearance.dark_mode:
            user_options.appearance.dark_mode = False
            utils.exec_sh(f"swww img {user_options.appearance.wallpaper_light} --transition-type wave --transition-fps 120 --transition-duration 1")
            utils.exec_sh("gsettings set org.gnome.desktop.interface color-scheme prefer-light")
        else:
            user_options.appearance.dark_mode = True
            utils.exec_sh(f"swww img {user_options.appearance.wallpaper_dark} --transition-type wave --transition-fps 120 --transition-duration 1")
            utils.exec_sh("gsettings set org.gnome.desktop.interface color-scheme prefer-dark")
        css_manager.reload_all_css()

