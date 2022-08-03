import math
import time
from array import array

import board
import digitalio
from audiobusio import PDMIN


class Mic(PDMIN):
    @staticmethod
    def mean(values):
        return sum(values) / len(values)

    @classmethod
    def normalized_rms(cls, values):
        minbuf = int(cls.mean(values))
        sum_of_samples = sum(
            float(sample - minbuf) * (sample - minbuf)
            for sample in values
        )
        return math.sqrt(sum_of_samples / len(values))

    def __init__(self):
        self.dpwr = digitalio.DigitalInOut(board.MIC_PWR)
        self.dpwr.direction = digitalio.Direction.OUTPUT
        self.dpwr.value = 1
        super().__init__(board.PDM_CLK, board.PDM_DATA,
                         sample_rate=16000,
                         bit_depth=16,
                         mono=True,
                         oversample=64,
                         startup_delay=0.11)

    def record(self, samples=10):
        super().record(samples, len(samples))
        return samples

    def record_norm(self, samples=10):
        samples = self.record(samples)
        magnitude = self.normalized_rms(samples)
        return magnitude

    def read(self, num_samples=10):
        samples = array('H', [0] * num_samples)
        return self.record(samples)

    def check(self, num_samples=10):
        return self.on_update(self.read(num_samples))

    def on_update(self, samples):
        pass

    def read_norm(self, num_samples=10):
        samples = self.read(num_samples)
        magnitude = self.normalized_rms(samples)
        return magnitude


def test_mic():
    from components import Display
    display = Display()
    display.clear()

    m = Mic()
    bitmap, tile_grid = display.bitmap(palette=['black', 'white', 'light_yellow', 'yellow', 'orange', 'red', 'dark_red'])
    samples = array('H', [0] * 10)

    while True:
        for x in range(240):
            v = m.record_norm(samples)
            vb = min([max([0, int(v)]), 239])
            y = 239 - vb
            c = 1 + int(vb/40)
            bitmap[x, y] = c
        time.sleep(1)
        bitmap.fill(0)


if __name__ == "__main__":
    test_mic()
