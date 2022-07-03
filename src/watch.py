import time
import board
import analogio
from test_gps import GPS, display, write_text, update_display, ExtendedDisplay, test_gps
from pulse import Pulse
from buttons import Button, VibMo, VibMoButton



class Watch(object):
    def __init__(self):
        self.gps = GPS(tx=board.D0, on_update=self.gps_update)
        self.display = ExtendedDisplay(native_frames_per_second=60)
        self.pulse = Pulse(pin=board.A3, avg_samples=100, med_window=50, beats=10, init_rate=60)
        self.pulse.on_value = self.pulse_reading
        self.vibmo_button = VibMoButton(pin=0)
        self.top_button = Button("A2")
        self.side_button = Button("A1")
        self.displayed_text = [""]*4

    @property
    def vibmo(self):
        self.vibmo_button.mode = "vibmo"
        return self.vibmo_button.vibmo

    @property
    def bottom_button(self):
        self.vibmo_button.mode = "button"
        return self.vibmo_button.button

    def clear(self):
        self.display.clear()
        self.bitmap = self.display.init_bitmap()

    def buzz(self):
        self.vibmo_button.buzz()

    def write_text(self, lines, scale=2, spacing=25, x_start=20, y_start=10, color=0xFFFFFF):
        self.clear()
        for i, line in enumerate(lines):
            self.display.write_text(line, scale, x_start, i*spacing + y_start, color=0xFFFFFF)

    def gps_update(self, **kw):
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
                self.displayed_text[lines.index(k)] = k + ": " + conversions[k](v)
        self.write_text(self.displayed_text)

    def pulse_reading(self, ind, value, dv, phase, new_phase):
        print(value, dv)
        offset = 120
        amp = 100
        self.bitmap[ind % 240, offset - int(amp * value)] = 1
        if not (ind % 240):
            self.clear()
            self.display.write_text(str(p.rate), 2, 40, 200, color=0xFFFFFF)
            time.sleep(0.5)
            self.clear()
            for x in range(240):
                self.bitmap[x, int(offset - 0.33 * amp)] = 1
                self.bitmap[x, offset] = 1
                self.bitmap[x, int(offset + 0.33*amp)] = 1# Write your code here :-)
