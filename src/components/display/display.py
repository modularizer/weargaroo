import time
import displayio
import terminalio

from adafruit_display_text import label
import adafruit_imageload

from components.display.st7789_display import ST7789Display


class Display(ST7789Display):
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

    def init_bitmap(self, palette_colors):
        if not palette_colors:
            palette_colors = (0, 0xFFFFFF)
        bitmap = displayio.Bitmap(self.width, self.height, len(palette_colors))
        palette = displayio.Palette(len(palette_colors))
        for i, c in enumerate(palette_colors):
            palette[i] = c
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)
        self.splash.append(tile_grid)
        return bitmap

    def show_image(self, fn):
        self.clear()
        image, palette = adafruit_imageload.load(fn, bitmap=displayio.Bitmap,
                                                 palette=displayio.Palette)
        palette.make_transparent(0)
        tile_grid = displayio.TileGrid(image, pixel_shader=palette)
        self.splash.append(tile_grid)


if __name__ == "__main__":
    display = Display()
    display.show_image("imgs/weargaroo_logo.bmp")
    while True:
        time.sleep(10)
