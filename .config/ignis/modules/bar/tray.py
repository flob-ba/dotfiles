from ignis import widgets
from ignis.services.system_tray import SystemTrayService, SystemTrayItem

tray = SystemTrayService.get_default()

class TrayItem(widgets.Button):
    def __init__(self, item: SystemTrayItem):
        super().__init__()
        self.css_classes = ["bar-system-tray-item"]
        self.child = widgets.Icon(icon_name = item.icon)

class SystemTray(widgets.Box):
    def __init__(self):
        super().__init__()
        self.child = tray.bind("items", lambda items: [TrayItem(item) for item in items])
