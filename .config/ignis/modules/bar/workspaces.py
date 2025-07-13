from ignis import widgets
from ignis.services.hyprland import HyprlandService, HyprlandMonitor, HyprlandWorkspace

hypr = HyprlandService.get_default()

class Workspace(widgets.Label):
    def __init__(self, workspace: HyprlandWorkspace, monitor_id: int):
        super().__init__(justify = "center")
        self.workspace = workspace
        self.monitor_id = monitor_id
        self.label = str(workspace.id)
        self.__update_css()
        hypr.connect("notify::active-workspace", lambda x,y : self.__update_css())
        hypr.monitors[monitor_id].connect("notify::active-workspace-id", lambda x,y: self.__update_css())


    def __update_css(self):
        self.css_classes = ["bar-workspace"]
        if hypr.active_workspace.id == self.workspace.id:
            self.add_css_class("active")
        if hypr.monitors[self.monitor_id].active_workspace_id == self.workspace.id:
            self.add_css_class("visible")

class Workspaces(widgets.Box):
    def __init__(self, monitor: int):
        super().__init__()
        self.vertical = True
        self.css_classes = ["bar-workspace-pill"]
        self.child = hypr.bind("workspaces", lambda workspaces: [Workspace(workspace, monitor) for workspace in filter(lambda workspace: workspace.monitor_id == monitor, workspaces)])

