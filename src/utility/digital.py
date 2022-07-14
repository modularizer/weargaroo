import digitalio


def DigitalOut(pin):
    digital_out = digitalio.DigitalInOut(pin)
    digital_out.direction = digitalio.Direction.OUTPUT
    return digital_out


def DigitalIn(pin):
    digital_out = digitalio.DigitalInOut(pin)
    digital_out.direction = digitalio.Direction.INPUT
    return digital_out