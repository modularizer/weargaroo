import storage
import time

class GPX(object):
    def __init__(self, rtc, timezone_offset, fn="logs/run_%TIME%.gpx", name=None):
        self.rtc = rtc
        self.timezone_offset = timezone_offset

        y,m,d,H,M,S,*_ = self.rtc.datetime
        s = f"{y}_{m}_{d}_{H}.{M}.{S}"
        fn = fn.replace("%TIME%", s)

        if name is None:
            name = fn.split("/")[-1].replace(".gpx","")

        self.fn = fn
        self.name = name

        self.s = ""

        try:
            storage.remount('/', False)
            time.sleep(0.1)
            self.mem = False
        except Exception as e:
            self.mem = True
            pass
        self.write(self.make_header(name))

        print("initialized gpx", fn, name)

    def write(self, s, mode="a"):
        if self.mem:
            if mode == "w":
                self.s = ""
            self.s += s
        else:
            with open(self.fn, mode) as f:
                f.write(s)

    def make_header(self, name):
        return f"""
<?xml version="1.0" encoding="UTF-8"?>
<gpx creator="StravaGPX" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd" version="1.1" xmlns="http://www.topografix.com/GPX/1/1">
  <trk>
    <name>{name}</name>
    <type>9</type>
      <trkseg>"""

    def make_point(self, lat, lng, alt):
        ts = time.localtime(time.mktime(self.rtc.datetime) - self.timezone_offset * 60 *60)
        y, m, d, H, M, S, *_ = ts
        return f"""
        <trkpt lat="{lat}" lon="-{lng}">
          <ele>{alt}</ele>
          <time>{y}-{m:02d}-{d:02d}T{H:02d}:{M:02d}:{S:02d}Z</time>
        </trkpt>"""

    def add_point(self, lat, lng, alt):
        s = self.make_point(lat, lng, alt)
        self.write(s,'a')

    def finish(self):
        s = """
    </trkseg>
  </trk>
</gpx>
"""
        self.write(s,'a')
        storage.remount('/', True)
