import displayio
import terminalio

from adafruit_display_text import label


from .st7789.display import Display as Display


class ExtendedDisplay(Display):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)

    def clear(self):
        # Make the display context
        self.splash = displayio.Group()
        self.show(self.splash)
        return self.splash

    def write_text(self, text="Hello World", scale=1, x=0, y=0, color=0xFFFFFF):
        # Draw a label
        text_group = displayio.Group(scale=scale, x=x, y=y)
        text_area = label.Label(terminalio.FONT, text=text, color=color)
        text_group.append(text_area)  # Subgroup for text scaling
        self.splash.append(text_group)
        return text_group

    def draw_rect(self, color=0xFFFFFF, width=240, height=240, x=0, y=0):
        color_bitmap = displayio.Bitmap(width, height, 1)
        color_palette = displayio.Palette(1)
        color_palette[0] = color
        bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=x, y=y)
        self.splash.append(bg_sprite)
        return bg_sprite

    def init_bitmap(self):
        bitmap = displayio.Bitmap(self.width, self.height, 2)
        palette = displayio.Palette(2)
        palette[0] = 0x000000
        palette[1] = 0xffffff
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)
        self.splash.append(tile_grid)
        return bitmap
