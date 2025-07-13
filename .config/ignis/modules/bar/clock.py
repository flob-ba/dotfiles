from ignis import widgets, utils
from ignis.variable import Variable
from datetime import datetime

class Clock(widgets.CenterBox):
    def __init__(self):
        super().__init__()
        
        self.hours = Variable(
            value = utils.Poll(1000, lambda _: datetime.now().strftime("%H")).bind("output"),
        )
        self.minutes = Variable(
            value = utils.Poll(1000, lambda _: datetime.now().strftime("%M")).bind("output"),
        
            )
        self.center_widget = widgets.Box(
            vertical = True,
            child = [
                widgets.Label(justify = "center", label = self.hours.bind("value")),    
                widgets.Label(justify = "center", label = self.minutes.bind("value")),    
            ],
        )
