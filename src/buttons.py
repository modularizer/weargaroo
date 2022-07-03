import time

import board
import analogio
import digitalio


class Button(object):
    def __init__(self, pin_name: str = "A0", push_callback=None, release_callback=None,
                hold_callback=None, condition=None, threshold=2500, comparison=">"):
        self.pin_name = pin_name
        self.pin = getattr(board, self.pin_name)
        self.analog_in = None
        self.last_state = False
        self.push_time = None
        self.count = 0
        if push_callback is not None:
            self.push_callback = push_callback
        if release_callback is not None:
            self.release_callback = release_callback
        if hold_callback is not None:
            self.hold_callback = hold_callback
        if condition is not None:
            if threshold is not None:
                condition = {
                    ">": lambda v: v > threshold,
                    ">=": lambda v: v >= threshold,
                    "<": lambda v: v < threshold,
                    "<=": lambda v: v <= threshold,
                    "==": lambda v: v == threshold,
                    "!=": lambda v: v != threshold,
                }[comparison]
            self.condition = condition

    def config(self):
        self.analog_in = analogio.AnalogIn(self.pin)
        return self.analog_in

    def read(self):
        if self.analog_in is not None:
            return self.analog_in.value

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
                t = time.time()
                dt = 0
                self.push_time = t
                self.push_callback(self.count, t, dt)
            elif is_triggered and not changed:
                t = time.time()
                dt = t - self.push_time
                self.hold_callback(self.count, t, dt)
            elif changed and not is_triggered:
                t = time.time()
                dt = t - self.push_time
                self.release_callback(self.count, t, dt)

    def push_callback(self, count, t, dt):
        print(f"{self.pin_name} pushed #{count}")

    def hold_callback(self, count, t, dt):
        print(f"{self.pin_name} pushed #{count} for {dt}s")

    def release_callback(self, count, t, dt):
        print(f"{self.pin_name} released #{count} after {dt}s")

    def deinit(self):
        if self.analog_in is not None:
            self.analog_in.deinit()


class Buttons(object):
    def __init__(self, buttons: dict):
        self.buttons = {k: v if isinstance(v, Button) else Button(k, **v) if isinstance(v, dict) else Button(k) for k, v in buttons.items()}

    def config(self):
        for v in self.buttons.values():
            v.config()

    def read(self):
        return {k: v.read() for k, v in self.buttons.items()}

    def is_triggered(self):
        return {k: v.is_triggered() for k, v in self.buttons.items()}

    def check(self):
        for v in self.buttons.values():
            v.check()

    def deinit(self):
        for v in self.buttons.values():
            v.deinit()


class VibMo(object):
    def __init__(self, pin_name):
        self.pin_name = pin_name
        self.pin = getattr(board, pin_name)
        self.digital_out = None

    def config(self):
        self.digital_out = digitalio.DigitalInOut(self.pin)
        self.digital_out.direction = digitalio.Direction.OUTPUT
        return self.digital_out

    def start(self):
        print("starting")
        if self.digital_out is not None:
            print("here")
            self.digital_out.value = 1

    def stop(self):
        print("stopping")
        if self.digital_out is not None:
            self.digital_out.value = 0

    def buzz(self, dt = 0):
        self.start()
        time.sleep(dt)
        self.stop()

    def deinit(self):
        if self.digital_out is not None:
            self.digital_out.deinit()

class VibMoButton(object):
    def __init__(self, num, *button_args, **button_kwargs):
        analog_pin_name = f"A{num}"
        digital_pin_name = f"D{num}"
        self.button = Button(analog_pin_name, *button_args, **button_kwargs)
        self.vibmo = VibMo(digital_pin_name)
        self._mode = None

    @property
    def mode(self):
        """vibmo or button"""
        return self._mode

    @mode.setter
    def mode(self, mode):
        changed = mode != self._mode
        if changed:
            self.config(mode)

    @property
    def active_component(self):
        if self._mode == "button":
            return self.button
        if self._mode == "vibmo":
            return self.vibmo

    def config(self, mode):
        if mode == "button":
            self.deinit()
            self.button.config()
        elif mode == "vibmo":
            self.deinit()
            self.vibmo.config()
        else:
            self.deinit()

    def __getattr__(self, item):
        if self._mode in ["button", "vibmo"]:
            return getattr(self.active_component, item)

    def __setattr__(self, item, value):
        if self._mode in ["button", "vibmo"]:
            return setattr(self.active_component, item, value)

    def deinit(self):
        self.active_component.deinit()
        self._mode = None

    def buzz(self, dt=0):
        self.mode = "vibmo"
        return self.buzz(dt)

    def check(self):
        self.mode = "button"
        return self.check()




if __name__ == "__main__":
    a3 = Button("A2")
    a3.config()

    d0 = VibMo("D0")
    d0.config()

    d0.value = 1
    time.sleep(1)
    d0.value = 0

    a3.push_callback = lambda *a: d0.start()
    a3.release_callback = lambda *a: d0.stop()

    #d0.value = 1

    # a1 = analogio.AnalogIn(board.A1)

    while True:
        a3.check()
        # print(a1.value)
        time.sleep(0.05)
