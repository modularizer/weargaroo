import board
import analogio

from utility import Colors, DigitalOut


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
    colors = Colors()

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
    def rgba(self):
        return (self.r, self.g, self.b, max([self.r, self.g, self.b]) / 255)

    @rgba.setter
    def rgba(self, rgba):
        r, g, b, a = rgba
        self.r = int(r * a / 255)
        self.g = int(g * a / 255)
        self.b = int(b * a / 255)

    @property
    def color(self):
        return self.colors.color_search(self.value)

    @color.setter
    def color(self, color: str):
        if hasattr(self.colors, color):
            self.value = getattr(self.colors, color)

    @property
    def value(self):
        return hex(self.r << 16 | self.g << 8 | self.b)

    @value.setter
    def value(self, value):
        self.r, self.g, self.b = self.colors.to_rgb(value)


if __name__ == "__main__":
    import time

    rgb = RGB_LED()

    while True:
        for k, v in rgb.colors.dict().items():
            print(k)
            rgb.value = v
            time.sleep(0.5)