from ignis import widgets
from ignis.services.notifications import NotificationService, Notification

notifyService = NotificationService.get_default()

class NotificationPopup(widgets.Box):
    def __init__(self, notification: Notification, popup_list: "NotificationPopupList"):
        super().__init__()
        self.css_classes = ["notification-popup"]
        self.popup_list = popup_list
        self.child = [
            widgets.Icon(
                image = notification.icon if notification.icon is not None else "dialog-information-symbolic",
                pixel_size = 30,
                css_classes = ["notification-popup-icon"],
            ),
            widgets.Box(
                vertical = True,
                child = [
                    widgets.Label(
                        justify = "left",
                        label = notification.summary[:57] + "..." if len(notification.summary) > 60 else notification.summary ,
                        css_classes = ["notification-popup-title"],
                    ),
                    widgets.Label(
                        justify = "left",
                        label = notification.body[:57] + "..." if len(notification.body) > 60 else notification.body,
                    ),
                ],
            ),
            widgets.CenterBox(
                vertical = True,
                center_widget = widgets.Button(
                    css_classes = ["notification-popup-dismiss-button"],
                    child = widgets.Icon(icon_name = "window-close-symbolic", pixel_size = 30),
                    on_click = lambda _: notification.dismiss(),
                ),
            ),
        ]
        notification.connect("dismissed", lambda _: self.__on_dismissed())

    def __on_dismissed(self):
        self.unparent()
        if len(notifyService.popups) == 0:
            self.popup_list.visible = False

class NotificationPopupList(widgets.Window):
    def __init__(self, monitor_id: int):
        super().__init__(f"ignis-notification-popup-list-{monitor_id}")
        self.anchor = ["top", "right", "bottom"]
        self.exclusivity = "ignore"
        self.visible = False
        self.monitor = monitor_id
        self.child = widgets.Box(
            css_classes = ["notification-popup-list"],
            vertical = True,
        )
        notifyService.connect("new_popup", lambda _, notification: self.__on_new_popup(notification))

    def __on_new_popup(self, notification: Notification):
        self.visible = True
        self.child.prepend(NotificationPopup(notification, self))

