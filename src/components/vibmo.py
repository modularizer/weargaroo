import time
import board
import digitalio

from components.button import Button
from utility.digital import DigitalOut


class VibMo(object):
    def __init__(self, num, config='digital'):
        self.num = num
        self.pin = getattr(board, f"D{num}")
        self.digital_out = None
        if config:
            self.config()

    def config(self):
        self.digital_out = DigitalOut(self.pin)
        return self.digital_out

    @property
    def value(self):
        return self.digital_out.value

    @value.setter
    def value(self, value):
        self.digital_out.value = value

    def start(self):
        if self.digital_out is None:
            self.config()
        self.value = 1

    def stop(self):
        self.value = 0

    def buzz(self, dt = 0):
        self.start()
        time.sleep(dt)
        self.stop()

    def deinit(self):
        if self.digital_out is not None:
            self.digital_out.deinit()
            self.digital_out = None

    def check(self):
        return self.value


def test_vibmo():
    vm = VibMo(0)

    while True:
        print("buzz")
        vm.buzz(1)
        time.sleep(1)


if __name__ == "__main__":
    test_vibmo()
