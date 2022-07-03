import time
import board
import digitalio

from components.button import Button


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
    b = Button("A2")
    b.config()

    vm = VibMo("D0")
    vm.config()

    vm.value = 1
    time.sleep(1)
    vm.value = 0

    b.push_callback = lambda *a: vm.start()
    b.release_callback = lambda *a: vm.stop()

    while True:
        b.check()
        time.sleep(0.05)
