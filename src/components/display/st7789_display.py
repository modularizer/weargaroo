import board
import displayio

from adafruit_st7789 import ST7789

import pinout


class ST7789Display(ST7789):
    @staticmethod
    def init_display_bus(baudrate=31250000, tft_cs=pinout.TFT_CS, reset=pinout.TFT_RST, tft_dc=pinout.TFT_DC,
                         polarity=1, phase=1):
        spi = board.SPI()
        while not spi.try_lock():
            pass
        spi.configure(baudrate=baudrate, polarity=polarity, phase=phase)
        spi.unlock()

        displayio.release_displays()
        # NOTE: MakerFocus TFT requires polarity=1, phase=1 (SPI_MODE3), if using another model of screen,
        # these may change
        display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=reset,
                                         polarity=polarity, phase=phase, baudrate=baudrate)
        display_bus.reset()
        return display_bus

    def __init__(self, width=240, height=240, rotation=180, rowstart=80,
                 baudrate=31250000, tft_cs=board.NFC2, reset=board.D4, tft_dc=board.D5, **kwargs):
        self.display_bus = self.init_display_bus(baudrate, tft_cs=tft_cs, reset=reset, tft_dc=tft_dc)
        super().__init__(self.display_bus, width=width, height=height, rowstart=rowstart, rotation=rotation, **kwargs)


