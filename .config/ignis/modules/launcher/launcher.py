from ignis import widgets
from ignis.window_manager import WindowManager
from ignis.services.applications import ApplicationsService, Application

applications = ApplicationsService.get_default()
window_manager = WindowManager.get_default()

class LauncherAppItem(widgets.Button):
    def __init__(self, app: Application, monitor_id: int):
        super().__init__()
        self.app = app
        self.monitor_id = monitor_id
        self.css_classes = ["launcher-app-item"]
        self.child = widgets.Box(
            child = [
                widgets.Icon(
                    css_classes = ["launcher-app-item-icon"],
                    image = app.icon,
                    pixel_size = 30
                ),
                widgets.Label(
                    label = app.name
                ),
            ]
        )
        self.on_click = lambda _: self.launch() 

    def launch(self):
        self.app.launch()
        window_manager.close_window(f"ignis-launcher-{self.monitor_id}")

class Launcher(widgets.RevealerWindow):
    def __init__(self, monitor_id: int):
        self.entry = widgets.Entry(
            css_classes = ["launcher-entry"],
            placeholder_text = "...",
            on_change = lambda x: self.__on_change(x.text),
            on_accept = lambda x: self.__on_accept(),
            hexpand = True
        )

        self.app_list = widgets.Box(
            vertical = True,
            visible = False,
        )

        revealer = widgets.Revealer(
            transition_type = "slide_down",
            transition_duration = 250,
            reveal_child = True,
            child = widgets.Box(
                css_classes = ["launcher"],
                vertical = True,
                child = [
                    widgets.Box(
                        child = [
                            widgets.Icon(
                                css_classes = ["launcher-search-icon"],
                                icon_name = "system-search-symbolic",
                                pixel_size = 25,
                            ),
                            self.entry
                        ],
                    ),
                    self.app_list,
                ],
            ),
        )

        super().__init__(
            namespace = f"ignis-launcher-{monitor_id}",
            revealer = revealer
        )
        self.monitor = monitor_id
        self.visible = False 
        self.popup = True
        self.anchor = ["top"]
        self.exclusivity = "ignore"
        self.layer = "top"
        self.kb_mode = "on_demand"
        self.child = widgets.Box(child = [revealer])
        
        self.connect("notify::visible", lambda _,x: self.__on_notify_visible())

    def __on_change(self, query: str):
        apps = applications.search(applications.apps, query)
        
        if len(apps) == 0:
            self.app_list.visible = False
            self.entry.grab_focus_without_selecting()
            self.app_list.child = []
        else:
            self.app_list.child = [LauncherAppItem(app, self.monitor) for app in apps[:5]]
            self.app_list.visible = True

    def __on_accept(self):
        if len(self.app_list.child) > 0:
            self.app_list.child[0].launch()
            self.entry.text = ""

    def __on_notify_visible(self):
        if not self.visible:
            self.entry.text = ""
        else:
            self.entry.grab_focus()
