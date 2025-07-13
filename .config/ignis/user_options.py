import os
from ignis.options_manager import OptionsManager, OptionsGroup
from ignis import DATA_DIR, CACHE_DIR

USER_OPTIONS_FILE = f"{DATA_DIR}/user_options.json"
OLD_USER_OPTIONS_FILE = f"{CACHE_DIR}/user_options.json"

class UserOptions(OptionsManager):
    def __init__(self):
        print(USER_OPTIONS_FILE)
        print(OLD_USER_OPTIONS_FILE)


        if not os.path.exists(USER_OPTIONS_FILE) and os.path.exists(OLD_USER_OPTIONS_FILE):
            with open(OLD_USER_OPTIONS_FILE) as f:
                data = f.read()
            with open(USER_OPTIONS_FILE, "w") as f:
                f.write(data)

        try:
            super().__init__(USER_OPTIONS_FILE)
        except FileNotFoundError:
            pass
        
    class Appearance(OptionsGroup):
        dark_mode: bool = True
        wallpaper_light: str = "/home/flob/.wallpaper/outset_day.jpg" 
        wallpaper_dark: str = "/home/flob/.wallpaper/outset_evening.jpg" 

    appearance = Appearance()

user_options = UserOptions()

