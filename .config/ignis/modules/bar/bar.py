from ignis import widgets
from .clock import Clock
from .status_pill import StatusPill
from .window import ActiveWindow
from .workspaces import Workspaces

class Bar(widgets.Window):
    def __init__(self, monitor: int):
        super().__init__(f"ignis-bar-{monitor}")
        self.monitor = monitor
        self.anchor = ["left", "top", "bottom"]
        self.exclusivity = "ignore"
        self.layer = "top"
        self.child = widgets.CenterBox(
            css_classes = ["bar"],
            vertical = True,
            start_widget = widgets.CenterBox(center_widget = widgets.Box(
                vertical = True,
                child = [
                    Workspaces(monitor),
                ]
            )),
            center_widget = widgets.CenterBox(center_widget = ActiveWindow(monitor)),
            end_widget = widgets.CenterBox(center_widget = widgets.Box(
                vertical = True,
                child = [
                    StatusPill(),
                    Clock(),
                ]
            )),
        )
