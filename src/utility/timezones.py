class TimeZoneFinder(object):
    def first_guess(self, lat, lat_ord, lng, lng_ord):
        direction = 1 if lng_ord == "E" else -1
        offset = direction * lng * 24 / 360
        print(offset)

    # TODO lookup timezones by lat/lng
    # TODO figure out if daylight savings is in effect