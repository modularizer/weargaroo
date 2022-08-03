import time
from watch import WatchState, Watch
from utility.mean_filt import MeanFilt

from utility.coords import dist


class RunningWatchState(WatchState):
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

            "lat": d.text("00.0", scale=2, x=10, y=10, color="blue"),
            "lat_ord": d.text("N", scale=2, x=100, y=10, color="dark_blue"),
            "lng": d.text("00.0", scale=2, x=130, y=10, color="green"),
            "lng_ord": d.text("W", scale=2, x=220, y=10, color="dark_green"),
            "alt": d.text("00.0", scale=2, x=10, y=40, color="yellow"),
            "alt_units": d.text("m", scale=2, x=100, y=40, color="dark_yellow"),

            "charge": d.text("??.?%", scale=2, x=180, y=40, color="pink"),
        }
        keys = ["lat", "lat_ord", "lng", "lng_ord", "alt", "alt_units", "last_gps_time",
                "year", "month", "day", "hour", "minute", "second", "weekday", "yearday", "is_dst",
                "heart_rate", "accel", "gyro", "top_button", "bottom_button", "side_button", "charge"]
        for key in keys:
            self.add_property(type(self), key)

        self.icons.update({
            "h": d.text("0", scale=3, x=10, y=190, color="white"),
            "c0": d.text(":", scale=3, x=28, y=190, color="white"),
            "m": d.text("00", scale=3, x=42, y=190, color="white"),
            "c1": d.text(":", scale=3, x=80, y=190, color="white"),
            "s": d.text("00", scale=3, x=95, y=190, color="white"),
            "d": d.text("0.00", scale=3, x=150, y=190, color="white")
        })

        extra = ["h", "m", "s", "d"]
        for key in extra:
            self.add_property(type(self), key)


    def format_m(self, m):
        return f"0{m}"[-2:]

    def format_s(self, s):
        return f"0{s}"[-2:]

    def format_d(self, d):
        return round(d, 2)

    def set_lat(self, v):
        if 'lat' not in self.state:
            self.state['lat'] = v
            self.icons["lat"].text = str(v)
        else:
            dv = abs(self.state['lat'].value - v.value)
            if abs(dv) < 0.1:
                self.state['lat'] = v
                self.icons["lat"].text = str(v)
            else:
                print(v, self.state['lat'])

    def set_lng(self, v):
        if 'lng' not in self.state:
            self.state['lng'] = v
            self.icons["lng"].text = str(v)
        else:
            dv = abs(self.state['lng'].value - v.value)
            if abs(dv) < 0.1:
                self.state['lng'] = v
                self.icons["lng"].text = str(v)

    def set_alt(self, a):
        if isinstance(a, (int, float)) and 0 <= a <= 15000:
            if 'alt' not in self.state:
                self.state['alt'] = a
                self.icons["alt"].text = a
            else:
                da = abs(self.state['alt'] - a)
                if da < 100:
                    self.state['alt'] = a
                    self.icons["alt"].text = a


class RunningWatch(Watch):
    WatchState = RunningWatchState

    def run(self):
        self.timing = False

        #self.gps.calibrate_rtc()
        while True:
            self.check_item(self.gps)
            #self.check_item(self.imu)
            self.check_item(self.battery)
            self.check_item(self.top_button)
            # self.check_item(self.side_button)

    def on_top_button_push(self, config, t, dt):
        try:
            if not self.timing:
                print("\n\nSTARTING\n\n")
                from utility.gpx import GPX
                lat = self.state.lat
                lng = self.state.lng
                alt = float(self.state.alt) if self.state.alt else 0
                self.state.h = 0
                self.state.m = 0
                self.state.s = 0
                self.distance = 0
                self.last_point = (lat, lng, alt)
                self.gpx = GPX(self.rtc, self.gps.timezone_offset)
                if not self.gpx.mem:
                    self.state.icons["h"].label.color = 0x00FF00
                    self.state.icons["m"].label.color = 0x00FF00
                    self.state.icons["s"].label.color = 0x00FF00
                self.timing = time.time()
        except Exception as e:
            print("error", e)
            pass

    def on_top_button_hold(self, config, t, dt):
        print("dt=", dt, self.timing)
        if self.timing and dt > 3:
            self.timing = False
            try:
                self.gpx.finish()
                self.state.icons["h"].label.color = 0xFF0000
                self.state.icons["m"].label.color = 0xFF0000
                self.state.icons["s"].label.color = 0xFF0000
            except Exception as e:
                self.display.clear()
                self.display.text(str(e), x=10, y=10, scale = 1)

    def on_top_button_release(self, *a):
        pass

    def on_gps_time_update(self, ts):
        super().on_gps_time_update(ts)
        if self.timing:
            dt = time.time() - self.timing
            h = int(dt/(60*60))
            m = int((dt/60)%60)
            s = int(dt % 60)
            if h != self.state.h:
                self.state.h = h
            if m != self.state.m:
                self.state.m = m
            if s != self.state.s:
                self.state.s = s
            lat = self.state.lat
            lng = self.state.lng
            alt = self.state.alt if self.state.alt is not None else 0
            d = dist(lat.value, lng.value, alt, self.last_point[0].value, self.last_point[1].value, self.last_point[2])
            # print("d=", d)
            self.distance += d
            self.state.d = self.distance/1609.34
            self.last_point = (lat, lng, alt)
            self.gpx.add_point(lat, lng, alt)


if __name__ == "__main__":
    w = RunningWatch()
