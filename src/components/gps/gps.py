import rtc
import time

from components.gps.gtu7 import GTU7
from components.gps.nmea import NMEA


class GPS(GTU7):
    def __init__(self, on_update=None, **kw):
        super().__init__(**kw)
        self.buffer = ""
        self._on_update = on_update
        self.position = GPSPosition(on_update)

    @property
    def on_update(self):
        return self._on_update

    @on_update.setter
    def on_update(self, on_update):
        self.position.on_update = on_update

    def clear(self):
        self.uart.read()
        self.position = GPSPosition(self.on_update)

    def read(self):
        message = super().read()
        if message is not None:
            messages = (self.buffer + message).split("$")
            self.buffer = messages[-1]
            new_messages = messages[:-1]
            for message in new_messages:
                if message:
                    self.receive(message)
                    return message

    def check(self):
        return self.read()

    def receive(self, message):
        return self.position.receive(message)

    def calibrate_rtc(self, timeout=10):
        self.position.calibrate_time = True
        t0 = time.time()
        while self.position.calibrate_time and time.time() < (t0 + timeout):
            self.read()

        if self.position.calibrate_time:
            print("timed out before clock was calibrated")
            return False
        print("rtc calibrated")
        print(self.position.time_dict)
        return self.position.time_dict

    @property
    def rtc(self):
        return self.position.rtc


class GPSPosition(object):
    def __init__(self, on_update=None, calibrate_time=True):
        self.lat = None
        self.lng = None
        self.alt = None
        self.calibrate_time = calibrate_time
        self.calibrated = False
        self.rtc = rtc.RTC()

        try:
            with open("timezone.txt") as f:
                self.timezone_offset = int(f.read())
        except:
            self.timezone_offset = -8

        self.time_dict = {
            "y": 0,
            "m": 0,
            "d": 0,
            "H": 0,
            "M": 0,
            "S": 0
        }
        self.on_update = on_update
        self.messages = []

    def receive(self, message):
        if message:
            t = time.time()
            print(message)
            data = NMEA.interpret_message(message)
            if data is not None:
                data["time_received"] = t
                if hasattr(self, data["type"]):
                    getattr(self, data["type"])(data["values"])
                else:
                    # print(data)
                    pass

    def GPGGA(self, values):
        print("received", values)
        try:
            self.update_lat(values['lat'])
            self.update_lng(values['lng'])
            self.update_alt(values['alt'])
            self.update_time(values['time'])
        except Exception as e:
            print(e)

    def GPGSV(self, values):
        sats = values['sats']
        if sats is not None:
            # print([(sat['satellite_prn'], (sat['elevation_degrees'], sat['azimuth'], sat['snr_db'])) for sat in sats])
            pass

    def update_lat(self, lat):
        print("lat=", lat)
        self.lat = lat
        if self.on_update:
            self.on_update(lat=self.lat)

    def update_lng(self, lng):
        self.lng = lng
        if self.on_update:
            self.on_update(lng=self.lng)

    def update_alt(self, alt):
        self.alt = alt
        if self.on_update:
            self.on_update(alt=self.alt)

    def update_time(self, t):
        y, m, d, H, M, S = t
        if y is None:
            y = 2000
        if m is None:
            m = 0
        if d is None:
            d = 0
        H = (H + self.timezone_offset) % 24
        td = {
            "y": y, "m": m, "d": d, "H": H, "M": M, "S": S
        }
        self.time_dict.update({k: v for k, v in td.items() if v is not None})
        td = self.time_dict
        ts = time.struct_time(
            (td["y"],
             td["d"],
             td["m"],
             td["H"],
             td["M"],
             td["S"],
             0,
             -1,
             -1)
        )
        t = time.mktime(ts)
        dt = time.time() - t
        if self.calibrate_time or abs(dt) > 30:
            print("calibrating clock")
            self.rtc.datetime = ts
            self.calibrate_time = False
            self.calibrated = True
        if self.on_update:
            self.on_update(time=self.time_dict)


def test_gps():
    import board
    import displayio
    from components import Display

    d = Display()

    g = d.group()
    text = d.text("Time:\nLat:\nLng\nAlt:\n", scale=2, x=50, y=40, color="gray")
    clock = d.text("", scale=2, x=120, y=40, color="white")
    lat = d.text("", scale=2, x=120, y=75, color="white")
    lng = d.text("", scale=2, x=120, y=110, color="white")
    alt = d.text("", scale=2, x=120, y=145, color="white")
    conversions = {
        "time": (clock, lambda td: f"{td['H']}:{td['M']}:{td['S']}"),
        "lat": (lat, lambda x: f"{x[0]} {x[1]}"),
        "lng": (lng, lambda x: f"{x[0]} {x[1]}"),
        "alt": (alt, lambda x: f"{x[0]} {x[1]}"),
    }

    def update_display(**kw):
        print("UPDATE", kw)
        for k, v in kw.items():
            if k in conversions and v is not None:
                t, f = conversions[k]
                t.text = f(v)

    gps = GPS(tx=board.D0, on_update=update_display)
    # gps.calibrate_rtc()

    while True:
        try:
            gps.read()
            time.sleep(0.05)
        except KeyboardInterrupt as ke:
            raise ke
        except Exception as e:
            print("err", e)


if __name__ == "__main__":
    test_gps()
