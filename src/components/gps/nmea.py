class NMEA(object):
    """
    This class is built with the purpose of decoding NMEA sentences received by the GPS module.
    Information about NMEA sentenctes can be found at http://aprs.gids.nl/nmea/#allgp.
    """

    @staticmethod
    def time(s):
        t = (None, None, None, int(s[0:2]), int(s[2:4]), int(float(s[4:])))
        return t

    @staticmethod
    def date(s):
        t = (2000 + int(s[0:2]), int(s[2:4]), int(float(s[4:])), None, None, None)
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
    }  # TODO add information for more types of NMEA sentences

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
            # print(message)
            pass
        else:
            msg, checksum, *extra = message.split("*")
            # TODO use checksum
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