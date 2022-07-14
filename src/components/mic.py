import math
import time
import array

import board
import digitalio
import audiobusio


class Mic(audiobusio.PDMIn):
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

    def record(self, samples):
        super().record(samples, len(samples))
        return samples

    def record_norm(self, samples):
        samples = self.record(samples)
        magnitude = self.normalized_rms(samples)
        return magnitude

    def read(self, num_samples):
        samples = array.array('H', [0] * num_samples)
        return self.record(samples)

    def read_norm(self, num_samples):
        samples = self.read(num_samples)
        magnitude = self.normalized_rms(samples)
        return magnitude


def test_mic():
    from components.display import Display
    display = Display(native_frames_per_second=60)
    display.clear()

    m = Mic()
    palette_colors = [0, 0x808080, 0xFFFFFF, 0xFFFF80, 0xFFFF00, 0xFF8000, 0xFF0000, 0x800000]
    samples = array.array('H', [0] * 10)

    while True:
        display.clear()
        bitmap = display.init_bitmap(palette_colors)
        for x in range(240):
            v = m.record_norm(samples)
            vb = min([max([0, int(v)]), 239])
            y = 239 - vb
            c = 1 + int(vb/40)
            bitmap[x, y] = c
            print(v, y, c)
        time.sleep(1)


if __name__ == "__main__":
    test_mic()
