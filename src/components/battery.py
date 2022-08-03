import board
from utility.mean_filt import MeanFilt

class Battery(object):
    def __init__(self):
        import analogio
        import digitalio
        self.vbatt = analogio.AnalogIn(board.VBATT)
        self.vbatt_en = digitalio.DigitalInOut(board.READ_BATT_ENABLE)
        self.vbatt_en.direction = digitalio.Direction.INPUT
        self.charge_status = digitalio.DigitalInOut(board.CHARGE_STATUS)
        self.charge_status.direction = digitalio.Direction.INPUT
        del analogio
        del digitalio
        self.last_value = None
        self.filt = MeanFilt(20)

    def start_charging(self):
        self.vbatt_en.value = True

    def stop_charging(self):
        self.vbatt_en.value = False

    @property
    def charge(self):
        r = self.vbatt.value/65535
        self.filt.append(r)
        v = self.filt.mean
        return round(1000*(v - 0.9), 2)

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
