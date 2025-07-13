from ignis import widgets
from ignis.services.audio import AudioService
from ignis.services.network import NetworkService
from ignis.services.upower import UPowerService

audio = AudioService.get_default()
network = NetworkService.get_default()
upower = UPowerService.get_default()

class Battery(widgets.Box):
    def __init__(self):
        super().__init__()
        self.css_classes = ["bar-status-pill-item"]
        self.vertical = True
        self.child = [
            widgets.Icon(
                icon_name = upower.devices[0].bind("icon_name"),
            ),
            widgets.Label(
                justify = "left",
                label = upower.devices[0].bind("percent", lambda percent: f"{int(percent)}"),
                style = "font-size: 11pt;"
            ),
        ]

class Microphone(widgets.Icon):
    def __init__(self):
        super().__init__()
        self.css_classes = ["bar-status-pill-item"]
        self.icon_name = audio.microphone.bind("icon_name")

class Speaker(widgets.Icon):
    def __init__(self):
        super().__init__()
        self.css_classes = ["bar-status-pill-item"]
        self.icon_name = audio.speaker.bind("icon_name")

class Wifi(widgets.Icon):
    def __init__(self):
        super().__init__()
        self.css_classes = ["bar-status-pill-item"]
        self.icon_name = network.wifi.bind("icon_name")

class StatusPill(widgets.Box):
    def __init__(self):
        super().__init__()
        self.css_classes = ["bar-status-pill"]
        self.vertical = True
        self.child = [
            Microphone(),
            Speaker(),
            Wifi(),
            Battery(),
        ]

