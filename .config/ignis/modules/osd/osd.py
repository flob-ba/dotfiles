from ignis import utils, widgets
from ignis.services.audio import AudioService
from ignis.services.backlight import BacklightService

audio = AudioService.get_default()
backlight = BacklightService.get_default()

class OSDMicrophone(widgets.Box):
    def __init__(self):
        super().__init__()
        self.css_classes = ["osd"]
        self.child = [
            widgets.Icon(
                css_classes = ["osd-icon"],
                icon_name = audio.microphone.bind("icon_name"),
                pixel_size = 25,
            ),
            widgets.Scale(
                css_classes = ["osd-slider"],
                vertical = False,
                min = 0,
                max = 100,
                step = 1,
                value = audio.microphone.bind_many(["volume", "is_muted"], lambda volume, is_muted : 0 if is_muted or volume is None else volume),
                hexpand = True,
            ),
        ]
        self.visible = False 

class OSDVolume(widgets.Box):
    def __init__(self):
        super().__init__()
        self.css_classes = ["osd"]
        self.child = [
            widgets.Icon(
                css_classes = ["osd-icon"],
                icon_name = audio.speaker.bind("icon_name"),
                pixel_size = 25,
            ),
            widgets.Scale(
                css_classes = ["osd-slider"],
                vertical = False,
                min = 0,
                max = 100,
                step = 1,
                value = audio.speaker.bind_many(["volume", "is_muted"], lambda volume, is_muted : 0 if is_muted or volume is None else volume),
                hexpand = True,
            ),
        ]
        self.visible = False 

class OSDBrightness(widgets.Box):
    def __init__(self):
        super().__init__()
        self.css_classes = ["osd"]
        self.child = [
            widgets.Icon(
                css_classes = ["osd-icon"],
                icon_name = "display-brightness-symbolic",
                pixel_size = 25,
            ),
            widgets.Scale(
                css_classes = ["osd-slider"],
                vertical = False,
                min = 0,
                max = backlight.devices[0].bind("max_brightness"),
                step = 1,
                value =  backlight.devices[0].bind("brightness"),
                hexpand = True,
            ),
        ]
        self.visible = False 

class OSD(widgets.Window):
    def __init__(self, monitor_id: int):
        super().__init__(f"ignis-osd-{monitor_id}")
        self.anchor = ["bottom"]
        self.exclusivity = "ignore"
        self.layer = "top"
        self.visible = False 
        self.monitor = monitor_id
        
        self.osd_microphone = OSDMicrophone()
        self.osd_volume = OSDVolume()
        self.osd_brightness = OSDBrightness()

        self.child = widgets.Box(
            vertical = True,
            child = [
                self.osd_microphone,
                self.osd_volume,
                self.osd_brightness,
            ],
        )

        audio.microphone.connect("notify::is-muted", lambda microphone, is_muted: self.__on_microphone_change())
        audio.microphone.connect("notify::volume", lambda microphone, volume: self.__on_microphone_change())
        audio.speaker.connect("notify::volume", lambda speaker, volume: self.__on_volume_change())
        audio.speaker.connect("notify::is-muted", lambda speaker, is_muted: self.__on_volume_change())
        backlight.devices[0].connect("notify::brightness", lambda device, brightness: self.__on_brightness_change())

        self.stay_visible_counts = 0
    
    def __on_microphone_change(self):
        self.visible = True
        self.osd_microphone.visible = True
        self.osd_brightness.visible = False
        self.osd_volume.visible = False 
        self.stay_visible_counts += 1
        utils.Timeout(ms = 3000, target = lambda: self.__request_hide())

    def __on_volume_change(self):
        self.visible = True
        self.osd_microphone.visible = False 
        self.osd_brightness.visible = False
        self.osd_volume.visible = True 
        self.stay_visible_counts += 1
        utils.Timeout(ms = 3000, target = lambda: self.__request_hide())
    
    def __on_brightness_change(self):
        self.visible = True
        self.osd_microphone.visible = False 
        self.osd_brightness.visible = True 
        self.osd_volume.visible = False 
        self.stay_visible_counts += 1
        utils.Timeout(ms = 3000, target = lambda: self.__request_hide())

    def __request_hide(self):
        self.stay_visible_counts -= 1
        self.osd_microphone.visible = False
        self.osd_volume.visible = False
        self.osd_brightness.visible = False
        if self.stay_visible_counts == 0:
            self.visible = False

