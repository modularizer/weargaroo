from rtc import RTC
import time
from busio import UART

import config

from utility.latlng import LatOrLng



class GPS(object):
    time_inaccuracy_allowed_s = 10

    @staticmethod
    def interp_time(s):
        return None, None, None, int(s[0:2]), int(s[2:4]), int(float(s[4:]))

    @staticmethod
    def interp_date(s):
        return (2000 + int(s[4:])), int(s[2:4]), int(float(s[0:2])), None, None, None

    @staticmethod
    def interp_lat(s):
        return LatOrLng(s)

    interp_lng = interp_lat
    interp_fix = lambda s: [None, "GPS", "DGPS"][int(s)]
    interp_dt_differential_correction = lambda s: float(s) if s else None
    interp_validity = lambda s: s == "A"
    interp_rel_true_north = lambda s: s == "T"

    info = {
        "GPGGA": {
            "description": "Global Positioning System Fix Data",
            "fields": [
                "time", "lat", "lat_ordinal", "lng", "lng_ordinal", "fix", "num_satellites",
                "horizontal_dilution_of_precision", "alt", "alt_units", "height_wgs84",
                "height_wgs84_units", "dt_differential_correction"
            ]
        },
        "GPGLL": {
            "description": "Geographical Position, Latitue/ Longiture and time",
            "fields": ["lat", "lat_ordinal", "lng", "lng_ordinal", "time", "validity"]
        },
        "GPRMC": {
            "description": "Recommended minimum specific GPS/Transit data",
            "fields": ["time", "validity", "lat", "lat_ordinal", "lng", "lng_ordinal",
                       "velocity_knots", "true_course", "date", "variation", "ordinal"]
        },
        "GPGSV": {
            "description": "GPS Satellites in view",
            "fields": [
                "num_messages", "message_number", "satellites_in_view",
                "satellite_prn_0", "elevation_degrees_0", "azimuth_0", "snr_db_0",
                "satellite_prn_1", "elevation_degrees_1", "azimuth_1", "snr_db_1",
                "satellite_prn_2", "elevation_degrees_2", "azimuth_2", "snr_db_2",
                "satellite_prn_3", "elevation_degrees_3", "azimuth_3", "snr_db_3",
            ]
        },
        "GPVTG": {
            "description": "Track Made Good and Ground Speed",
            "fields": [
                "track_made_good", "rel_true_north", "not_used", "not_used", "velocity_knots",
                "fixed_n", "velocity_kph", "fixed_k"
            ]
        }
    }  # TODO add information for more types of NMEA sentences

    def __init__(self, tx=config.GPS_TX, rx=config.GPS_RX):
        self.uart = UART(tx=tx, rx=rx, baudrate=9600, parity=None, stop=1)
        self.buffer = ""
        self.state = {}
        self.lat = None
        self.lng = None
        self.alt = None
        self.calibrated = False
        self.rtc = RTC()
        self.last_time = 0

        try:
            with open("timezone.txt") as f:
                self.timezone_offset = int(f.read())
        except:
            self.timezone_offset = -8

        self.messages = []

    def clear(self):
        self.uart.read()

    def check(self):
        return self.read()

    def read(self, num_bytes=32):
        try:
            data = self.uart.read(num_bytes)
            if data is not None:
                messages = (self.buffer + data.decode()).split("$")
                self.buffer = messages[-1]
                new_messages = messages[:-1]
                for message in new_messages:
                    if "*" in message:
                        msg, checksum, *extra = message.split("*")
                        # print(msg)
                        valid = self.checksum(msg, checksum)
                        if valid:
                            info = self.interpret_message(msg)
                            if info is not None:
                                info["time_received"] = time.time()
                                # print(info)
                                if hasattr(self, info["type"]) and info["values"] is not None:
                                    getattr(self, info["type"])(info["values"])
        except UnicodeError as e:
            pass

    def checksum(self, msg, checksum):
        c = 0
        for m in msg:
            c ^= ord(m)
        cs = hex(c)[2:].upper()
        checksum = checksum.strip()
        valid = cs == checksum
        return valid

    def interpret_message(self, message):
        sections = message.split(",")
        message_type = sections[0]
        info = {
            "type": message_type,
        }

        if message_type in self.info:
            fields = self.info[message_type]["fields"]
            info.update({
                "recognized": True,
                "description": self.info[message_type]["description"]
            })
            values = {}
            cls = type(self)
            for i, section in enumerate(sections[1:]):
                if i < len(fields):
                    name = fields[i]
                    if hasattr(cls, f"interp_{name}"):
                        v = getattr(cls, f"interp_{name}")(section)
                    else:
                        v = cls.interp_section(section)
                else:
                    name = i
                    v = cls.interp_section(section)
                if name != "not_used":
                    values[name] = v
            info["values"] = values
        else:
            info["recognized"] = False
            info["values"] = [self.interp_section(section) for section in sections]
        return info

    @staticmethod
    def interp_section(section):
        if section and all(v in "0123456789" for v in section):
            return int(section)
        if section and all(v in ".0123456789" for v in section):
            return float(section)
        return section

    def GPGSV(self, values):
        pass

    def GPGGA(self, values):
        self.update_lat(values["lat"], values["lat_ordinal"])
        self.update_lng(values["lng"], values["lng_ordinal"])
        self.update_alt(values["alt"], values["alt_units"])
        self.update_time(values["time"])

    def GPRMC(self, values):
        self.update_lat(values["lat"], values["lat_ordinal"])
        self.update_lng(values["lng"], values["lng_ordinal"])
        t = values["date"][:3] + values["time"][3:]
        self.update_time(t)

    def GPGLL(self, values):
        self.update_lat(values["lat"], values["lat_ordinal"])
        self.update_lng(values["lng"], values["lng_ordinal"])
        self.update_time(values["time"])

    def update_lat(self, lat, lat_ordinal):
        self.state["lat"] = lat
        self.state["lat_ordinal"] = lat_ordinal
        self.on_lat_update(lat, lat_ordinal)

    def update_lng(self, lng, lng_ordinal):
        self.state["lng"] = lng
        self.state["lng_ordinal"] = lng_ordinal
        self.on_lng_update(lng, lng_ordinal)

    def update_alt(self, alt, alt_units):
        self.state['alt'] = alt
        self.state['alt_units'] = alt_units
        self.on_alt_update(alt, alt_units)

    def update_velocity(self, velocity_knots):
        self.state["velocity_knots"] = velocity_knots
        self.on_velocity_update(velocity_knots)

    def update_time(self, ymdhms):
        rtc_dt = self.rtc.datetime
        y, m, d, H, M, S = [ymdhms[i] if ymdhms[i] is not None else rtc_dt[i] for i in range(6)]
        ts = time.struct_time(
            (y,
             m,
             d,
             H,
             M,
             S,
             rtc_dt[-3],
             rtc_dt[-2],
             rtc_dt[-1])
        )
        t = time.mktime(ts)
        if ymdhms[3] is not None:
            t += self.timezone_offset*60*60
            ts = time.localtime(t)
        # print(ts)
        if t < 1658500000:
            raise Exception(f"incorrect time: {t}, {ts}")
        dt = t - self.last_time
        if (not self.calibrated) or dt > self.time_inaccuracy_allowed_s:
            self.last_time = t
            # print("rtc", self.rtc.datetime)
            try:
                old = time.mktime(self.rtc.datetime)
            except Exception as e:
                print("error", self.rtc.datetime)
                old = t
            dt = old - t
            if (not self.calibrated) or dt > self.time_inaccuracy_allowed_s:
                print("calibrating clock", dt, t, old)
                self.rtc.datetime = ts
                self.calibrated = True

                if self.on_time_calibration:
                    self.on_time_calibration(self.rtc.datetime)

        self.on_time_update(self.rtc.datetime)

    def calibrate_rtc(self, timeout=10):
        self.calibrated = False
        t0 = time.time()
        while (not self.calibrated) and time.time() < (t0 + timeout):
            self.read()

        if not self.calibrated:
            raise Exception("timed out before clock was calibrated")
        return self.rtc.datetime

    def on_lat_update(self, lat, ord):
        pass

    def on_lng_update(self, lng, ord):
        pass

    def on_alt_update(self, alt, ord):
        pass

    def on_time_update(self, ts):
        pass

    def on_time_calibration(self, ts):
        pass

    def on_velocity_update(self, v):
        pass


def test_gps():
    import board
    import displayio
    from components.display import Display

    d = Display()

    g = d.group()
    text = d.text("Time:\nLat:\nLng\nAlt:\n", scale=2, x=50, y=40, color="gray")
    clock = d.text("", scale=2, x=120, y=40, color="white")
    lat = d.text("", scale=2, x=120, y=75, color="white")
    lng = d.text("", scale=2, x=120, y=110, color="white")
    alt = d.text("", scale=2, x=120, y=145, color="white")

    gps = GPS()
    gps.calibrate_rtc(60)

    def time_update(ts):
        clock.text = f"{ts[3]}:{ts[4]}:{ts[5]}"

    def lat_update(v, u):
        lat.text = f"{v} {u}"

    def lng_update(v, u):
        lng.text = f"{v} {u}"

    def alt_update(v, u):
        alt.text = f"{v} {u}"

    gps.on_time_update = time_update
    gps.on_lat_update = lat_update
    gps.on_lng_update = lng_update
    gps.on_alt_update = alt_update

    while True:
        gps.read()
        time.sleep(2)


if __name__ == "__main__":
    # test_gps()
    gps = GPS()
    while True:
        try:
            gps.read()
        except:
            pass
