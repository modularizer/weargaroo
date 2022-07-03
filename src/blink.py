import time
import board
import digitalio
import analogio

board_attrs = [
'LED', 'BLUE_LED', 'GREEN_LED', 'RED_LED', # LEDs
'6D_INT1', '6D_PWR', '6D_SCL', '6D_SDA', # 6 Axis IMU
'A0', 'A1', 'A2', 'A3', 'A4', 'A5', # Analog Pins
'D0', 'D1', 'D10', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', # Digital Pins
'NFC1', 'NFC2', # NFC antenna
'MIC_PWR', 'PDM_CLK', 'PDM_DATA', # Microphone
'SPI', 'MISO', 'MOSI', 'SCK', # SPI
'I2C', 'SCL', 'SDA', # I2C
'UART', 'TX', 'RX' # UART
]


class MyBoard(object):
    def __init__(self):
        for name in ["LED", "BLUE_LED", "GREEN_LED", "RED_LED"]:
            self._make_digital_pin_property(name, direction="OUTPUT")

        for i in range(10):
            name = f"D{i}"
            self._make_digital_pin_property(name, direction="unassigned")

        for i in range(6):
            name = f"A{i}"
            self._make_analog_pin_property(name, direction="unassigned")

    def _make_digital_pin_property(self, name, direction="INPUT"):
        direction = getattr(digitalio.Direction, direction.upper())
        pin = getattr(board, name.upper())
        _value = None
        _name = "_" + name.lower()
        setattr(self, _name, _value)

        def fget(*a):
            _value = getattr(self, _name, None)
            if _value is None:
                _value = digitalio.DigitalInOut(pin)
                _value.direction = direction
                setattr(self, _name, _value)
            return _value

        def fget_out(*a):
            _value = getattr(self, _name, None)
            if _value is None:
                _value = digitalio.DigitalInOut(pin)
                setattr(self, _name, _value)
            if _value.direction != digitalio.Direction.OUTPUT:
                _value.direction = digitalio.Direction.OUTPUT
            return _value

        def fget_in(*a):
            _value = getattr(self, _name, None)
            if _value is None:
                _value = digitalio.DigitalInOut(pin)
                setattr(self, _name, _value)
            if _value.direction != digitalio.Direction.INPUT:
                _value.direction = digitalio.Direction.INPUT
            return _value

        def fset(*a, value):
            _value = fget()
            if _value.direction == digitalio.Direction.OUTPUT:
                _value.value = value

        def fdel(*a):
            _value = getattr(self, _name, None)
            if _value is not None:
                _value.deinit()
            setattr(self, _name, None)

        prop = property(fget, fset, fdel)
        prop_out = property(fget_out, fset, fdel)
        prop_in = property(fget_in, fset, fdel)
        setattr(type(self), name.lower(), prop)
        setattr(type(self), name.lower() + "_out", prop)
        setattr(type(self), name.lower() + "_in", prop)

    def _make_analog_pin_property(self, name, direction="INPUT"):
        pin_types = {
            "OUTPUT": analogio.AnalogOut,
            "INPUT": analogio.AnalogIn
        }
        pin = getattr(board, name.upper())
        _value = None
        _name = "_" + name.lower()
        setattr(self, _name, _value)

        def fget(*a, pin_type=None):
            if pin_type is not None:
                pin_type = pin_types[direction]
            _value = getattr(self, _name, None)

            if _value is not None and not isinstance(_value, pin_type):
                _value.deinit()
                _value = None

            if _value is None:
                _value = pin_type
                setattr(self, _name, _value)

            return _value

        def fget_out(*a):
            return fget(pin_type=analogio.AnalogOut)

        def fget_in(*a):
            return fget(pin_type=analogio.AnalogIn)

        def fset(*a, value):
            _value = fget()
            if isinstance(_value, analogio.AnalogOut):
                _value.value = value

        def fdel(*a):
            _value = getattr(self, _name, None)
            if _value is not None:
                _value.deinit()
            setattr(self, _name, None)

        prop = property(fget, fset, fdel)
        prop_out = property(fget_out, fset, fdel)
        prop_in = property(fget_in, fset, fdel)
        setattr(type(self), name.lower(), prop)
        setattr(type(self), name.lower() + "_out", prop)
        setattr(type(self), name.lower() + "_in", prop)

m = MyBoard()



while True:
    m.led.value = True
    time.sleep(0.5)
    m.led.value = False
    time.sleep(0.5)
