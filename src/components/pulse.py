import time
import board
import analogio
import supervisor

from utility import MeanFilt
import pinout


class AnalogPulse(object):
    def __init__(self, pin=pinout.PULSE):
        self.analog_in = analogio.AnalogIn(pin)

    @property
    def analog_value(self):
        return self.analog_in.value

    def read(self):
        val = self.analog_value
        t = supervisor.ticks_ms() / 1000
        return val, t


class Pulse(AnalogPulse):
    def __init__(self, pin=board.A3, avg_samples=100, med_window=50, beats=10, init_rate=60):
        super().__init__(pin)
        self.beats = beats
        self.avg_samples = avg_samples
        self.avg_sum = 0
        self.avg_length = 0
        self.mean = MeanFilt(med_window)
        self.tracked_phases = (1,)
        self.filtered_period = MeanFilt(beats * len(self.tracked_phases))
        init_period = 60 / init_rate
        for _ in range(beats * 4):
            self.filtered_period.append(init_period)
        self.last_phase_times = [None] * 4
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
            self.last_y = y

            if y > 0.33:
                phase = 1
            elif y < -0.33:
                phase = 3
            elif self.last_phase == 3:
                phase = 0
            else:
                phase = 2
            new_phase = phase != self.last_phase
            if new_phase:
                last_phase_time = self.last_phase_times[phase]
                if last_phase_time is not None:
                    dpt = t - last_phase_time
                    if dpt > 0.5*self.period:
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


def test_pulse():
    from .display import Display
    display = Display(native_frames_per_second=60)
    display.clear()

    p = Pulse()
    a1 = analogio.AnalogIn(board.A1)

    global bitmap
    bitmap = display.init_bitmap()

    def on_value(ind, value, dv, phase, new_phase):
        global bitmap
        print(value, dv)
        # y = max([0, min([239, 120 - int(200 * dv)])])
        y = max([0, min([239, 120 - int(100 * value)])])
        bitmap[ind % 240, y] = 1
        if not (ind % 240):
            display.clear()
            display.write_text(str(p.rate), 2, 40, 200, color=0xFFFFFF)
            time.sleep(0.5)
            display.clear()
            bitmap = display.init_bitmap()
            for x in range(240):
                bitmap[x, 80] = 1
                bitmap[x, 120] = 1
                bitmap[x, 160] = 1

    p.on_value = on_value

    while True:
        p.read()


if __name__ == "__main__":
    test_pulse()

