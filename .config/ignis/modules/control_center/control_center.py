from ignis import widgets
from .user import UserInfo
from .quick_settings import QuickSettings

class ControlCenter(widgets.RevealerWindow):
    def __init__(self, monitor_id: int):
        revealer = widgets.Revealer(
            transition_type = "slide_down",
            transition_duration = 250,
            reveal_child = True,
            child = widgets.Box(
                css_classes = ["control-center"],
                vertical = True,
                child = [
                    UserInfo(),
                    QuickSettings(),
                ],
            ),
        )
        
        super().__init__(
            namespace = f"ignis-control-center-{monitor_id}",
            revealer = revealer,
        )
        self.monitor = monitor_id
        self.visible = False 
        self.popup = True
        self.anchor = ["top", "left"]
        self.exclusivity = "ignore"
        self.layer = "top"
        self.kb_mode = "on_demand"
        self.margin_left = 40
        self.child = widgets.Box(child = [revealer])
