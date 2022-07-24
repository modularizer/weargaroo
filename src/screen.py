from components import Display
from base_watch import BaseWatch, BaseWatchState


class Screen(BaseWatchState):
    lat = None
    lat_ord = None
    lng = None
    lng_ord = None
    alt = None
    alt_units = None
    last_gps_time = None

    year = None
    day = None
    month = None
    hour = None
    minute = None
    second = None
    weekday = None
    yearday = None
    is_dst = None

    heart_rate = None

    accel = (0, 0, -9.82)
    gyro = (0, 0, 0)

    top_button = 0
    side_button = 0
    bottom_button = 0

    charge = None

    def __init__(self, watch):
        self.watch = watch

        d = watch.display
        self.icons = {
            "hour": d.text("12", scale=4, x=40, y=120, color="green"),
            "colon": d.text(":", scale=4, x=120, y=120, color="white"),
            "minute": d.text("00", scale=4, x=130, y=120, color="blue"),
        }



class Watch(BaseWatch):
    WatchState = Screen