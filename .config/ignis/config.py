import os
from ignis import utils
from ignis.options import options
from ignis.css_manager import CssManager, CssInfoPath
from ignis.services.wallpaper import WallpaperService
from modules import Bar
from user_options import user_options

css_mananger = CssManager.get_default()

def patch_style_scss(path: str):
    with open(path) as file:
        contents = file.read()

    with open(os.path.join(utils.get_current_dir(), "scss/colors-dark.scss" if user_options.appearance.dark_mode else "scss/colors-light.scss")) as file:
        color_contents = file.read()

    return utils.sass_compile(string = color_contents + contents, extra_args = ["--load-path", utils.get_current_dir()])

css_mananger.apply_css(
    CssInfoPath(
        name = "main",
        path = os.path.join(utils.get_current_dir(), "style.scss"),
        compiler_function = patch_style_scss
    )
)

if user_options.appearance.dark_mode:
    utils.exec_sh(f"swww img {user_options.appearance.wallpaper_dark} --transition-type wave --transition-fps 120 --transition-duration 1")
    utils.exec_sh("gsettings set org.gnome.desktop.interface color-scheme prefer-dark")
else:
    utils.exec_sh(f"swww img {user_options.appearance.wallpaper_light} --transition-type wave --transition-fps 120 --transition-duration 1")
    utils.exec_sh("gsettings set org.gnome.desktop.interface color-scheme prefer-light")

for i in range(utils.get_n_monitors()):
    Bar(i)

