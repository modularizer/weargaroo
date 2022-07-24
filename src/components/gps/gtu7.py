import board
import busio

import config


class GTU7(object):
    def __init__(self, tx=config.GPS_TX, rx=config.GPS_RX):
        self.uart = busio.UART(tx=tx, rx=rx, baudrate=9600, parity=None, stop=1)

    def read(self, num_bytes=32):
        try:
            data = self.uart.read(num_bytes)
            if data is not None:
                message = data.decode()
                return message
        except:
            pass


if __name__ == "__main__":
    import time

    gtu7 = GTU7()

    while True:
        m = gtu7.read()
        print(m)
        time.sleep(1)
