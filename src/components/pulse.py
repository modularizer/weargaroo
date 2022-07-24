import time
import board
import analogio
import supervisor

from utility import MeanFilt
import config


class AnalogPulse(object):
    def __init__(self, num=config.PULSE):
        pin = getattr(board, f"A{num}")
        self.analog_in = analogio.AnalogIn(pin)

    @property
    def analog_value(self):
        return self.analog_in.value

    def read(self):
        val = self.analog_value
        t = supervisor.ticks_ms() / 1000
        return val, t


class Pulse(AnalogPulse):
    def __init__(self, num=config.PULSE, avg_samples=40, med_window=40, beats=10, init_rate=60):
        super().__init__(num)
        self.beats = beats
        self.avg_samples = avg_samples
        self.avg_sum = 0
        self.avg_length = 0
        self.mean = MeanFilt(med_window)
        self.tracked_phases = (1,)
        self.num_phases = 5
        self.filtered_period = MeanFilt(beats * len(self.tracked_phases))
        init_period = 60 / init_rate
        for _ in range(beats * self.num_phases):
            self.filtered_period.append(init_period)
        self.last_phase_times = [None] * self.num_phases
        self.last_phase = None
        self.last_y = 0
        self.i = 0

    @property
    def rate(self):
        return 60 / self.period

    @property
    def period(self):
        return self.filtered_period.mean

    def read(self):
        val, t = super().read()
        if self.avg_length < self.avg_samples:
            self.avg_sum += val
            self.avg_length += 1
            return None
        else:
            avg_val = self.avg_sum / self.avg_length
            self.avg_sum = 0
            self.avg_length = 0
            self.mean.append(avg_val)
            med_val = self.mean.mean
            max_val = self.mean.max
            min_val = self.mean.min

            if max_val > min_val:
                y = (avg_val - self.mean.mean) / (max_val - min_val)
                y = max([-1, min([1, y])])
            else:
                y = 0

            dy = y - self.last_y
            pulse_dir = dy > 0
            self.last_y = y

            if y > 0.33:
                phase = 1 - 1 * pulse_dir
            elif y < -0.33:
                phase = 3 + 1 * pulse_dir
            elif self.last_phase == 4:
                phase = 0
            else:
                phase = 2
            new_phase = self.last_phase is None or phase == (self.last_phase + 1) % self.num_phases
            if new_phase:
                last_phase_time = self.last_phase_times[phase]
                if last_phase_time is not None:
                    dpt = t - last_phase_time
                    if dpt > 0.5 * self.period:
                        if phase in self.tracked_phases:
                            self.filtered_period.append(dpt)
                self.last_phase_times[phase] = t
                self.last_phase = phase

        # print(avg_val/self.mean.mean, self.mean.max/self.mean.mean, self.mean.min/self.mean.mean)
        self.on_value(self.i, y, dy, phase, new_phase)
        self.i += 1
        return y

    def on_value(self, ind, value, dy, phase, new_phase):
        print(ind, value, phase, new_phase)

    def check(self):
        return self.read()


def test_pulse():
    from components import Display
    display = Display()

    p = Pulse()

    bitmap, tile_grid = display.bitmap(width=240, height=240, palette=['black', 'white', 'light_red', 'red'])

    lines = display.group(display.line(y=80, color="red", show=False),
                          display.line(y=120, color="white", show=False),
                          display.line(y=160, color="red", show=False),
                          )
    pulse = display.text("60", x=50, y=200, scale=2)

    def on_value(ind, value, dv, phase, new_phase):
        y = max([0, min([239, 120 - int(120 * value)])])
        c = 3 if phase == 1 and new_phase else 2 if phase == 1 else 1
        x = ind % 240
        bitmap[x, y] = c
        if c == 3:
            for dx in [-2, -1, 1, 2]:
                if 0 <= (x + dx) <= 239:
                    for dy in [-2, -1, 1, 2]:
                        if 0 <= (y + dy) <= 239:
                            bitmap[x + dx, y + dy] = c
            pulse.text = str(p.rate)

        if not (ind % 240):
            bitmap.fill(0)

    p.on_value = on_value

    while True:
        # time.sleep(1)
        p.read()


if __name__ == "__main__":
    test_pulse()
