import time
from base_watch import BaseWatch, BaseWatchState


class WatchState(BaseWatchState):
    short_day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    short_month_names = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    def __init__(self, watch):
        self.watch = watch

        d = watch.display
        self.state = {}
        self.icons = {
            "weekday": d.text("Sun", scale=2, x=10, y=80, color="gray"),
            "month": d.text("Jan", scale=2, x=60, y=80, color="gray"),
            "day": d.text("1", scale=2, x=110, y=80, color="gray"),

            "hour": d.text("12", scale=8, x=10, y=120, color="deep_champagne"),
            "colon": d.text(":", scale=8, x=100, y=120, color="gainsboro"),
            "minute": d.text("00", scale=8, x=140, y=120, color="deep_champagne"),

            "lat": d.text("00.0", scale=1, x=150, y=10, color="blue"),
            "lat_ord": d.text("N", scale=1, x=195, y=10, color="dark_blue"),
            "lng": d.text("00.0", scale=1, x=150, y=25, color="green"),
            "lng_ord": d.text("W", scale=1, x=195, y=25, color="dark_green"),
            "alt": d.text("00.0", scale=1, x=150, y=40, color="yellow"),
            "alt_units": d.text("m", scale=1, x=195, y=40, color="dark_yellow"),

            "accel": d.text("0.0", scale=1, x=10, y=10, color="purple"),
            "au": d.text("m/s2", scale=1, x=100, y=10, color="dark_purple"),
            "gyro": d.text("0.0", scale=1, x=10, y=25, color="cyan"),
            "gu": d.text("rad/s", scale=1, x=100, y=25, color="dark_cyan"),
            "charge": d.text("??.?%", scale=1, x=10, y=40, color="pink"),

            "top_button": d.text("0.00", scale=1, x=210, y=10, color="red"),
        }
        keys = ["lat", "lat_ord", "lng", "lng_ord", "alt", "alt_units", "last_gps_time",
                "year", "month", "day", "hour", "minute", "second", "weekday", "yearday", "is_dst",
                "heart_rate", "accel", "gyro", "top_button", "bottom_button", "side_button", "charge"]
        for key in keys:
            self.add_property(type(self), key)

    def format_hour(self, h):
        return f" {((h - 1) % 12) + 1}"[-2:]

    def format_minute(self, m):
        return f"0{m}"[-2:]

    def format_second(self, s):
        self.icons["colon"].hidden = not self.icons["colon"].hidden
        return f"0{s}"[-2:]

    def format_weekday(self, wd):
        return self.short_day_names[wd]

    def format_month(self, mo):
        return self.short_month_names[mo]

    def format_accel(self, a):
        f = lambda n: f" {round(n, 1)}" if n > 0 else str(round(n, 1))
        return ",".join([f(v) for v in a])

    def format_gyro(self, g):
        f = lambda n: f" {round(n, 1)}" if n > 0 else str(round(n, 1))
        return ",".join([f(v) for v in g])

    def format_top_button(self, dt):
        return str(round(dt, 2))

    def add_property(self, T, key):
        def fget(_):
            return self.state[key] if key in self.state else None

        def fset(_, value):
            if hasattr(self, f"format_{key}"):
                value = getattr(self, f"format_{key}")(value)

            if hasattr(self, f"set_{key}"):
                getattr(self, f"set_{key}")(value)
            else:
                if key in self.icons:
                    self.icons[key].value = value
                self.state[key] = value

        p = property(fget, fset)
        print("adding property", key)
        setattr(T, key, p)


class Watch(BaseWatch):
    WatchState = WatchState

    def check_item(self, item):
        try:
            item.check()
        except KeyboardInterrupt as ke:
            raise ke
        except Exception as e:
            print(e)
            #raise e

    def run(self):
        self.timing = False
        self.gps.calibrate_rtc()
        while True:
            self.check_item(self.gps)
            self.check_item(self.imu)
            self.check_item(self.battery)
            self.check_item(self.battery)


if __name__ == "__main__":
    w = Watch()
