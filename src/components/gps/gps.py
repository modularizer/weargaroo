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

    def receive(self, message):
        return self.position.receive(message)


class GPSPosition(object):
    def __init__(self, on_update=None, calibrate_time=True):
        self.lat = None
        self.lng = None
        self.alt = None
        self.calibrate_time = calibrate_time
        self.rtc = rtc.RTC()
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
        self.update_lat(values['lat'])
        self.update_lng(values['lng'])
        self.update_alt(values['alt'])
        self.update_time(values['time'])

    def GPGSV(self, values):
        sats = values['sats']
        if sats is not None:
            #print([(sat['satellite_prn'], (sat['elevation_degrees'], sat['azimuth'], sat['snr_db'])) for sat in sats])
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
        td = {
            "y": y, "m": m, "d": d, "H": H, "M": M, "S": S
        }
        print(td)
        self.time_dict.update({k: v for k, v in td.items() if v is not None})
        if self.calibrate_time:
            td = self.time_dict
            ts = time.struct_time(
                (td["y"],
                td["d"],
                td["m"],
                td["H"],
                td["M"],
                td["S"],
                -1,
                -1,
                -1)
            )
            self.rtc.datetime = ts
            self.calibrate_time = False
        if self.on_update:
            self.on_update(time=self.time_dict)


if __name__ == "__main__":
    gps = GPS()

    t0 = time.time()
    while time.time() < (t0 + 10):
        gps.read()


