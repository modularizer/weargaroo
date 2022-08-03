import time

from components.button import Button
from components.vibmo import VibMo


class VibMoButton(object):
    def __init__(self, num, *button_args, config="button", **button_kwargs):
        self.button = Button(num, *button_args, config=False, **button_kwargs)
        self.vibmo = VibMo(num, config=False)
        self._mode = None
        self.config(config)

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
            self._mode = mode
        elif mode == "vibmo":
            self.deinit()
            self.vibmo.config()
            self._mode = mode
        else:
            self.deinit()
            self._mode = None

    def __getattr__(self, item):
        if self._mode in ["button", "vibmo"]:
            return getattr(self.active_component, item)

    def __setattr__(self, item, value):
        if self._mode in ["button", "vibmo"]:
            return setattr(self.active_component, item, value)

    def deinit(self):
        if self.active_component is not None:
            self.active_component.deinit()
        self._mode = None

    def buzz(self, dt=0):
        self.mode = "vibmo"
        return self.buzz(dt)

    def check(self):
        self.mode = "button"
        return self.check()


def test_vibmo_button():
    vmb = VibMoButton(0, config="button")

    while True:
        if vmb.check():
            vmb.buzz(1)
        else:
            time.sleep(0.1)


if __name__ == "__main__":
    test_vibmo_button()
