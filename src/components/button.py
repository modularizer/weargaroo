import time
import supervisor
import digitalio

import board


class Button(object):
    def __init__(self, num, push_callback=None, release_callback=None, hold_callback=None,
                 mode='digital', condition=None, threshold=0.001, comparison="<", config=False):
        self._mode = mode
        self.num = num
        self.pin = None
        self.last_state = False
        self.push_time = None
        self.count = 0
        if push_callback is not None:
            self.push_callback = push_callback
        if release_callback is not None:
            self.release_callback = release_callback
        if hold_callback is not None:
            self.hold_callback = hold_callback
        if threshold is not None:
            condition = {
                ">": lambda v: v > threshold,
                ">=": lambda v: v >= threshold,
                "<": lambda v: v < threshold,
                "<=": lambda v: v <= threshold,
                "==": lambda v: v == threshold,
                "!=": lambda v: v != threshold,
            }[comparison]
        if condition is not None:
            self.condition = condition
        if config:
            self.config(mode)

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode):
        self.config(mode)

    def config(self, mode=None):
        if mode is None:
            mode = self.mode
        self._mode = mode
        if mode == "analog":
            import analogio
            self.pin = analogio.AnalogIn(getattr(board, f"A{self.num}"))
            del analogio
        elif mode == "digital":
            from utility.digital import DigitalIn
            self.pin = DigitalIn(getattr(board, f"D{self.num}"))
            del DigitalIn
            if self.condition(0):
                self.pin.pull = digitalio.Pull.UP
            elif self.condition(1):
                self.pin.pull = digitalio.Pull.DOWN
        return self.pin

    def read(self):
        if self.pin is None:
            self.config()
        if self.mode == "digital":
            return self.pin.value
        elif self.mode == "analog":
            return self.pin.value / 65535

    @staticmethod
    def condition(value):
        return value < 2000

    def is_triggered(self):
        value = self.read()
        # print(value)
        if value is not None:
            return self.condition(value)

    def check(self):
        is_triggered = self.is_triggered()
        if is_triggered is not None:
            changed = self.last_state != is_triggered
            self.last_state = is_triggered
            if changed and is_triggered:
                self.count += 1
                t = supervisor.ticks_ms()
                dt = 0.001
                self.push_time = t
                self.push_callback(self.count, t, dt)
            elif is_triggered and not changed:
                t = supervisor.ticks_ms()
                dt = (t - self.push_time)/1000
                self.hold_callback(self.count, t, dt)
            elif changed and not is_triggered:
                t = supervisor.ticks_ms()
                dt = (t - self.push_time)/1000
                self.release_callback(self.count, t, dt)
        return is_triggered

    def push_callback(self, count, t, dt):
        print(f"{self.pin_name} pushed #{count}")

    def hold_callback(self, count, t, dt):
        print(f"{self.pin_name} pushed #{count} for {dt}s")

    def release_callback(self, count, t, dt):
        print(f"{self.pin_name} released #{count} after {dt}s")

    def deinit(self):
        if self.analog_in is not None:
            self.analog_in.deinit()
        elif self.digital_in is not None:
            self.digital_in.deinit()


def test_button():
    from components import Display
    import config

    d = Display()
    last = 0
    t = d.text("0", stroke=4)
    colors = [0x00ff00, 0xff0000]
    b = Button(config.TOP_BUTTON)

    while True:
        v = b.check()
        if v != last:
            t.text = str(v)
            t.color = colors[v]
            last = v
        time.sleep(0.05)


if __name__ == "__main__":
    # test_button()
    import time
    import config
    b = Button(config.TOP_BUTTON)

    while True:
        print(b.is_triggered())
        time.sleep(0.1)
