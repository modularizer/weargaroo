import time

from components.display import Display
from components.gps import GPS


class Clock(object):
    def __init__(self, mode="HH:MM:SS", twenty_four=False, gps=None, display=None):
        self.mode = mode
        self.twenty_four = twenty_four
        if gps is None:
            gps = GPS()
        if not gps.position.calibrated:
            gps.calibrate_rtc(timeout=60)
        if display is None:
            display = Display()
        self.display = display

    def check(self, mode=None):
        if mode is None:
            mode = self.mode
        st = time.localtime()
        print(st)
        y, d, m, H, M, S, wd, yd, is_dst = st
        if not self.twenty_four:
            H %= 12
        d = {
            "wkd": ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"][wd],
            "wd": ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"][wd],
            "yyyy": str(y),
            "yy": str(y)[2:],
            "dd": str(100 + d)[1:],
            "d": str(d),
            "mm": str(100 + m)[1:],
            "m": str(m),
            "HH": str(100 + H)[1:],
            "MM": str(100 + M)[1:],
            "SS": str(100 + S)[1:],
        }
        t = mode
        for k in d:
            t = t.replace(k, d[k])

        time_until = 1 if "S" in mode else 60 - S if "M" in mode else (60 - M) * 60 + 60 - S if "H" in mode else (
                                                                                                                             24 - H) * 60 * 60 + (
                                                                                                                             60 - M) * 60 + 60 - S
        return t, time_until

    def write(self, t):
        self.display.clear()
        self.display.write_text(t, scale=5, x=40, y=100)

    def update(self):
        t, time_until = self.check()
        self.write(t)
        return time_until

    def run(self):
        while True:
            try:
                t, time_until = self.check()
                self.write(t)
                time.sleep(time_until)
                # time.sleep(5)
            except Exception as e:
                print(e)


def test_clock():
    c = Clock("HH:MM")
    c.run()


if __name__ == "__main__":
    test_clock()