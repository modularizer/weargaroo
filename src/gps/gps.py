import rtc
import time

from .gtu7 import GTU7


class NMEA(object):
    """http://aprs.gids.nl/nmea/#allgp"""

    @staticmethod
    def time(s):
        t = (None, None, None, int(s[0:2]), int(s[2:4]), float(s[4:]))
        return t

    @staticmethod
    def date(s):
        t = (2000 + int(s[0:2]), int(s[2:4]), float(s[4:]), None, None, None)
        return t

    @staticmethod
    def lat(s):
        a, b = s.split(".")
        return int(a[:-2]) + int(a[-2:]) / 60 + float("0." + b) / 60

    lng = lat
    fix = lambda s: [None, "GPS", "DGPS"][int(s)]
    dt_differential_correction = lambda s: float(s) if s else None
    validity: lambda s: s == "A"
    rel_true_north: lambda s: s == "T"

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
    }

    @staticmethod
    def GPGSV(values):
        sats = [{}] * 4
        for k in ["satellite_prn", "elevation_degrees", "azimuth", "snr_db"]:
            for i in range(4):
                ki = f"{k}_{i}"
                if ki in values:
                    sats[i][k] = values[ki]
                    del values[ki]
                else:
                    sats[i][k] = None

        if all(sats[i]["satellite_prn"] is None for i in range(4)):
            sats = None
        values['sats'] = sats
        return values

    @staticmethod
    def GPGGA(values):
        try:
            for d in ["lat", "lng"]:
                o = f'{d}_ordinal'
                values[d] = (values[d], values[o])
                values[f'{d}_str'] = f"{values[d][0]} {values[o]}"
                del values[o]
            values['alt'] = (values['alt'], values['alt_units'])
            values['alt_str'] = f"{values['alt'][0]} {values['alt_units']}"
            del values['alt_units']

            values["lat_lng_str"] = f"{values['lat_str']}, {values['lng_str']} @ {values['alt_str']}"
        except Exception as e:
            #print(e, values)
            pass
        return values

    @classmethod
    def interpret_message(cls, message):
        if "*" not in message:
            print(message)
        else:
            msg, checksum, *extra = message.split("*")

            sections = msg.split(",")
            message_type = sections[0]
            info = {
                "type": message_type,
                "checksum": checksum.replace("\n", "").replace("\r", "")
            }

            if message_type in cls.info:
                fields = cls.info[message_type]["fields"]
                info.update({
                    "recognized": True,
                    "description": cls.info[message_type]["description"]
                })
                values = {}
                for i, section in enumerate(sections[1:]):
                    try:
                        if i < len(fields):
                            name = fields[i]
                            if hasattr(cls, name):
                                v = getattr(cls, name)(section)
                            else:
                                v = cls.interp_section(section)
                        else:
                            name = i
                            v = cls.interp_section(section)
                    except Exception as e:
                        print("error", i, section, e)
                        name = i
                        v = section
                    if name != "not_used":
                        values[name] = v
                if hasattr(cls, message_type):
                    values = getattr(cls, message_type)(values)
                info["values"] = values
            else:
                info["recognized"] = False
                info["values"] = [cls.interp_section(section) for section in sections]
            return info

    @staticmethod
    def interp_section(section):
        if section and all(v in "0123456789" for v in section):
            return int(section)
        if section and all(v in ".0123456789" for v in section):
            return float(section)
        return section


class GPSPosition(object):
    def __init__(self, on_update=None, calibrate_time=True):
        self.lat = None
        self.lng = None
        self.alt = None
        self.calibrate_time = True
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


if __name__ == "__main__":
    gps = GPS()

    t0 = time.time()
    while time.time() < (t0 + 10):
        gps.read()


