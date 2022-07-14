import displayio

from config import width, height


class ColorPalette(displayio.Palette):
    width = width
    height = height

    # 0/black
    _black = 0x000000

    # 1/white
    _white = 0xffffff

    # 2/dark
    cafe_noir = 0x4e3b2d
    deep_champagne = 0xedcb96

    # 3/light
    lavendar_blue = 0xedcb96
    gainsboro = 0xe4dde3

    # 4/info
    steel_teal = 0x488286
    viridian_green = 0x129490

    # 5/warning
    cerise = 0xd73364
    china_pink = 0xe56399

    def __init__(self, **colors_dict):
        colors_dict.update({
            "black": self._black,
            "white": self._white
        })
        self._palette = [0] * len(colors_dict)
        for ind, (color_name, color) in enumerate(colors_dict.items()):
            self.get_color(ind, color_name, color)
        super().__init__(len(self._palette))

    def get_color(self, ind, color_name, color):
        if isinstance(color, str):
            color = getattr(self, color)

        def fget():
            return self[ind]

        self._palette[ind] = color

        setattr(type(self), color_name, property(fget))

    def bitmap(self):
        return displayio.Bitmap(self.width, self.height, len(self._palette))

    def tile_grid(self):
        bitmap = self.bitmap()
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=self)
        return tile_grid, bitmap

    def splash(self):
        splash = displayio.Group()
        tile_grid, bitmap = self.tile_grid()
        splash.append(tile_grid)
        return splash, tile_grid, bitmap


class CustomPalettes(object):
    brown_rose = ColorPalette(
                    dark='cafe_noir',
                    light='deep_champagne',
                    bright='gainsboro',
                    info='viridian_green',
                    warning='china_pink'
                )
