from ignis import widgets
from ignis.css_manager import CssManager
from ignis.options import options
from ignis import utils
from user_options import user_options

css_manager = CssManager().get_default()

class DarkModeToggle(widgets.Button):
    def __init__(self):
        super().__init__()
        self.child = widgets.Icon(icon_name = "weather-clear-night")
        self.on_click = lambda _: self.__on_click()

    def __on_click(self):
        if user_options.appearance.dark_mode:
            user_options.appearance.dark_mode = False
            utils.exec_sh("gsettings set org.gnome.desktop.interface color-scheme prefer-light")
            options.wallpaper.set_wallpaper_path(user_options.appearance.wallpaper_light)
        else:
            user_options.appearance.dark_mode = True
            utils.exec_sh("gsettings set org.gnome.desktop.interface color-scheme prefer-dark")
            options.wallpaper.set_wallpaper_path(user_options.appearance.wallpaper_dark)
        css_manager.reload_all_css()

