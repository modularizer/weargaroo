import board
import displayio

from adafruit_st7789 import ST7789

import config


class ST7789Display(ST7789):
    @staticmethod
    def init_display_bus(baudrate=config.TFT_BAUDRATE, tft_cs=config.TFT_CS, reset=config.TFT_RST, tft_dc=config.TFT_DC,
                         polarity=config.TFT_POLARITY, phase=config.TFT_PHASE):
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

    def __init__(self, width=config.TFT_WIDTH, height=config.TFT_HEIGHT, rotation=config.TFT_ROTATION,
                 baudrate=config.TFT_BAUDRATE, tft_cs=config.TFT_CS, reset=config.TFT_RST, tft_dc=config.TFT_DC, **kwargs):
        self.display_bus = self.init_display_bus(baudrate, tft_cs=tft_cs, reset=reset, tft_dc=tft_dc)
        rowstart = 320 - height
        super().__init__(self.display_bus, width=width, height=height, rowstart=rowstart, rotation=rotation, **kwargs)


