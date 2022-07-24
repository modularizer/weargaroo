import board
import analogio

from utility import DigitalOut
from components.display.colors import get_color


class LED(object):
    def __init__(self, pin):
        self.digital_out = DigitalOut(pin)

    _value = True

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self.digital_out.value = value == 0


class RGB_LED(object):
    R = LED(board.LED_RED)
    G = LED(board.LED_GREEN)
    B = LED(board.LED_BLUE)

    @property
    def r(self):
        return self.R.value

    @r.setter
    def r(self, r):
        self.R.value = r

    @property
    def g(self):
        return self.G.value

    @g.setter
    def g(self, g):
        self.G.value = g

    @property
    def b(self):
        return self.B.value

    @b.setter
    def b(self, b):
        self.B.value = b

    @property
    def rgb(self):
        return (self.r, self.g, self.b)

    @rgb.setter
    def rgb(self, rgb):
        self.r, self.g, self.b = rgb

    @property
    def color(self):
        return self.rgb

    @color.setter
    def color(self, color):
        color = get_color(color)
        b = color % (1 << 8)
        g = (color >> 8) % (1<<8)
        r = color >> 16
        self.rgb = (r, g, b)

    def check(self):
        return self.rgb


def test_rgb_led():
    import time

    rgb = RGB_LED()

    while True:
        for color in ["red", "white", "blue", "green", "yellow","pink","black"]:
            rgb.color = color
            time.sleep(0.5)


if __name__ == "__main__":
    test_rgb_led()