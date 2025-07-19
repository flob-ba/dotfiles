import time
from ignis import utils, widgets
from ignis.services.hyprland import HyprlandService
from ignis.services.mpris import MprisService, MprisPlayer
from user_options import user_options

hypr = HyprlandService.get_default()
mpris = MprisService.get_default()

IGNORED_PLAYER_IDENTITIES = ["Mozilla zen"]

def filter_players(players: [MprisPlayer]):
    result = []
    for player in players:
        ignored = False
        for ignored_identity in IGNORED_PLAYER_IDENTITIES:
            if player.identity == ignored_identity:
                ignored = True
        if not ignored:
            result.append(player)
    return result

class MediaPopup(widgets.Revealer):
    def __init__(self, player: MprisPlayer):
        super().__init__()
        self.transition_type = "slide_down"
        self.transition_duration = 500
        self.reveal_child = False
        self.player = player
        self.css_classes = ["media-popup-shadow"]
        self.child = widgets.Box(css_classes = ["media-popup"], child = [
            widgets.Box(
                css_classes = ["media-popup-album-art-container"],
                child = [
                    widgets.Picture(
                        css_classes = ["media-popup-album-art"],
                        image = player.bind("art_url"),
                        width = 75,
                        height = 75,
                        content_fit = "cover",
                    ),
                ],
            ),
            widgets.Box(
                css_classes = ["media-popup-details-container"],
                vertical = True,
                child = [
                    widgets.Label(
                        css_classes = ["media-popup-title"],
                        label = player.bind("title")
                    ),
                    widgets.Label(label = player.bind("album")),
                    widgets.Label(label = player.bind("artist")),
                ]
            ),
        ])
        player.connect("notify::metadata", lambda player, metadata: self.__on_new_song())

    def __on_new_song(self):
        if hypr.active_window.class_name == self.player.identity or user_options.do_not_disturb:
            return

        utils.Timeout(ms = 1000, target = lambda: self.set_reveal_child(True))
        utils.Timeout(ms = 6000, target = lambda: self.set_reveal_child(False))

class MediaPopupList(widgets.Window):
    def __init__(self, monitor_id: int):
        super().__init__(f"ignis-media-popup-list-{monitor_id}")
        self.anchor = ["top"]
        self.exclusivity = "ignore"
        self.visible = True
        self.monitor = monitor_id
        self.child = widgets.Box(
            vertical = True,
            child = mpris.bind("players", lambda players: [MediaPopup(player) for player in filter_players(players)])
        )
