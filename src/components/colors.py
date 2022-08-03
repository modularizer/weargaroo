import displayio

BLACK = 0x000000
WHITE = 0xffffff
RED = 0xff0000
GREEN = 0x00ff00
BLUE = 0x0000ff
YELLOW = 0xffff00
ORANGE = 0xffff80
PINK = 0xff00ff
PURPLE = 0x8000ff
CYAN = 0x00ffff
GRAY = 0x808080
LIGHT_RED = 0xff8080
LIGHT_GREEN = 0x80ff80
LIGHT_BLUE = 0x8080ff
DARK_RED = 0x800000
DARK_GREEN = 0x008000
DARK_BLUE = 0x000080
LIGHT_YELLOW=0xffff80
LIGHT_PINK=0xff80ff
LIGHT_CYAN = 0x80ffff
DARK_YELLOW = 0x808000
DARK_PINK = 0x800080
DARK_CYAN = 0x008080
DARK_PURPLE = 0x400080

CAFE_NOIR = 0x4e3b2d
DEEP_CHAMPAGNE = 0xedcb96
LAVENDAR_BLUE = 0xedcb96
GAINSBORO = 0xe4dde3
STEEL_TEAL = 0x488286
VIRIDIAN_GREEN = 0x129490
CERISE = 0xd73364
CHINA_PINK = 0xe56399


def get_color(color):
    if color is None:
        return
    if isinstance(color, str):
        color = color.upper()
        if color in globals():
            return globals()[color]
        try:
            return int(color, 16)
        except:
            pass
    if isinstance(color, tuple) and len(color)==3 and all(isinstance(c, int) and 0 <= c <= 255 for c in color):
        return (color[0] << 16) | (color[1] << 8) | (color[2])
    if isinstance(color, int) and 0 <= color <= 0xFFFFFF:
        return color
    raise Exception(f"Unrecognized color: {color}")


def get_colors(colors):
    if isinstance(colors, (list, set, tuple)):
        return type(colors)([get_color(color) for color in colors])
    if isinstance(colors, dict):
        return {name: get_color(color) for name, color in colors.items()}
    raise Exception(f"Unsupported colors type: {type(colors)}")


def set_color(name, color):
    assert isinstance(name, str), f"name must be of type str, not {type(name)}"
    name = name.upper()
    color = get_color(color)
    globals()[name] = color


def set_colors(colors):
    assert isinstance(colors, dict), f"colors must be of type dict, not {type(colors)}"
    for name, color in colors.items():
        set_color(name, color)


class ColorPalette(displayio.Palette):
    def __new__(cls, *colors):
        if colors and len(colors)==1 and isinstance(colors[0], (list, tuple, set)) and not (len(colors[0]) ==3 and all(isinstance(c, int) and 0 <= c <= 255 for c in colors)):
            colors = colors[0]
        colors = get_colors(colors)
        p = displayio.Palette(len(colors))
        for i, color in enumerate(colors):
            p[i] = color
        return p


if __name__ == "__main__":
    bw = ColorPalette('black', 'white')
