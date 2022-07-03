import displayio
import terminalio
import time
import board

from gps.gps import GPS
from components.display import Display

display = Display(native_frames_per_second = 1)
display.clear()

displayed_text = ["", "", "", ""]


def write_text(lines, scale=2, spacing=25, x_start=20, y_start=10, color=0xFFFFFF):
    display.clear()
    for i, line in enumerate(lines):
        display.write_text(line, scale, x_start, i*spacing + y_start, color=0xFFFFFF)


def update_display(**kw):
    print("kw=", kw)
    lines = ["time", "lat", "lng", "alt"]
    conversions = {
        "time": lambda td: f"{td['H']}:{td['M']}:{td['S']}",
        "lat": lambda x: f"{x[0]} {x[1]}",
        "lng": lambda x: f"{x[0]} {x[1]}",
        "alt": lambda x: f"{x[0]} {x[1]}",
    }
    for k, v in kw.items():
        if k in lines and v is not None:
            displayed_text[lines.index(k)] = k + ": " + conversions[k](v)
    write_text(displayed_text)


def test_gps():
    gps = GPS(tx=board.D0, on_update=update_display)

    t0 = time.time()
    while True:
        try:
            gps.read()
        except KeyboardInterrupt as ke:
            raise ke
        except Exception as e:
            print("err", e)


if __name__ == "__main__":
    test_gps()

# Write your code here :-)
