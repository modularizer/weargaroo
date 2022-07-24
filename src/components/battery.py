import board
import analogio
import digitalio


class Battery(object):
    def __init__(self):
        self.vbatt = analogio.AnalogIn(board.VBATT)
        self.vbatt_en = digitalio.DigitalInOut(board.READ_BATT_ENABLE)
        self.vbatt_en.direction = digitalio.Direction.INPUT
        self.charge_status = digitalio.DigitalInOut(board.CHARGE_STATUS)
        self.charge_status.direction = digitalio.Direction.INPUT
        self.last_value = None

    def start_charging(self):
        self.vbatt_en.value = True

    def stop_charging(self):
        self.vbatt_en.value = False

    @property
    def charge(self):
        return round(self.vbatt.value / 655.35, 2)

    def check(self):
        v = self.charge
        if v != self.last_value:
            try:
                self.on_update(v)
            finally:
                self.last_value = v

    def on_update(self, charge):
        pass

    def __str__(self):
        return f"{self.charge} %"


def test_battery():
    import time
    from components import Display

    d = Display()
    t = d.text("", scale=4)

    b = Battery()
    while True:
        t.text = f"{b.charge} %"
        time.sleep(0.5)


if __name__ == "__main__":
    test_battery()