from ignis import widgets
from ignis.services.hyprland import HyprlandService, HyprlandWindow

hypr = HyprlandService.get_default()

class ActiveWindow(widgets.Box):
    def __init__(self, monitor: int):
        super().__init__()
        self.vertical = True
        self.child = hypr.bind("active_window", lambda active_window: [
            widgets.Label(justify = "left", label = c, css_classes = ["bar-active-window-title-char"]) for c in (active_window.title[:57] + "..." if len(active_window.title) > 60 else active_window.title)
        ])



