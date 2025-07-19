from ignis import utils, widgets
from ignis.services.fetch import FetchService
from user_options import user_options

fetch = FetchService.get_default()

username = utils.exec_sh("whoami").stdout[:-1]

class UserInfo(widgets.Box):
    def __init__(self):
        super().__init__()

        uptime = widgets.Label(halign = "start", css_classes = ["control-center-user-info-uptime"])
        utils.Poll(timeout = 1000, callback = lambda _: uptime.set_label(f"{fetch.uptime[0]} Days, {fetch.uptime[1]} Hours, {fetch.uptime[2]} Minutes, {fetch.uptime[3]} Seconds"))

        self.child = [
            widgets.Picture(
                css_classes = ["control-center-profile-picture"],
                image = user_options.profile_picture_location,
                width = 75,
                height = 75,
                content_fit = "cover",
            ),
            widgets.Box(
                css_classes = ["control-center-user-info-container"],
                vertical = True,
                child = [
                    widgets.Label(
                        label = f"Hello, {username}!",
                        halign = "start",
                    ),
                    uptime,
                ],
            ),
        ]
