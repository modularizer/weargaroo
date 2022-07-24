import time
import displayio

from components.display.st7789_display import ST7789Display
from components.display.colors import ColorPalette, get_color


class Display(ST7789Display):
    default_show = True

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.splash = self.clear()
        self.palettes = {
            "default": ColorPalette('black', 'white')
        }

    def clear(self):
        # Make the display context
        self.splash = displayio.Group()
        self.show(self.splash)
        return self.splash

    @property
    def hidden(self):
        return self.splash.hidden

    @hidden.setter
    def hidden(self, hidden):
        self.splash.hidden = hidden

    def get_group(self, group=None):
        if group is None:
            group = self.splash
        if not isinstance(group, displayio.Group):
            raise Exception(f"group not found: {group}")
        return group

    def hide(self, group=None):
        group = self.get_group(group)
        group.hidden = True

    def __getitem__(self, item):
        return self.splash[item]

    def index(self, layer=-1):
        if layer == "top":
            layer = -1
        elif layer == "bottom":
            layer = 0

        if isinstance(layer, int) and 0 <= layer < len(self.splash):
            ind = layer
        else:
            ind = self.splash.index(layer)
        return ind

    def pop(self, layer=-1):
        ind = self.index(layer)
        layer = self.splash.pop(ind)
        return layer

    def remove(self, layer=-1):
        return self.pop(layer)

    def insert(self, index, layer):
        if index == "top" or index == -1 or index == len(self.splash):
            self.splash.append(layer)
        elif index == "bottom" or index == 0:
            self.splash.prepend(layer)
        else:
            index = min([index, len(self.splash)])
            self.splash.insert(index, layer)

    def move(self, layer='splash', x=0, y=0, z=None, relative=False):
        if layer == "splash":
            layer = self.splash
        else:
            ind = self.index(layer)
            layer = self.splash[ind]
            if z is not None:
                self.splash.pop(ind)
                if z == "up":
                    z = ind
                if z == "down":
                    z = max([0, ind - 2])
                if relative and isinstance(z, int):
                    z = min([max([0, ind + z]), len(self.splash) - 1])
                self.insert(z, layer)
        if x is not None:
            if relative:
                layer.x = layer.x + x
            else:
                layer.x = x
        if y is not None:
            if relative:
                layer.y = layer.y + y
            else:
                layer.y = y

    def display(self, item=None, show=True, group=None):
        if show is None:
            show = self.default_show
        if show:
            group = self.get_group(group)
            group.hidden = False
            if item:
                item.hidden = False
                group.append(item)

    def group(self, *items, scale=1, x=0, y=0, show=None, hidden=False, group=None):
        item = displayio.Group(scale=scale, x=x, y=y)
        item.hidden = hidden
        for i in items:
            item.append(i)
        self.display(item=item, show=show, group=group)
        return item

    def palette(self, palette=None, *a):
        if isinstance(palette, displayio.Palette):
            return palette
        if palette is None:
            return self.palettes["default"]
        if isinstance(palette, str) and palette in self.palettes:
            return self.palettes[palette]
        return ColorPalette(palette, *a)

    def bitmap(self, width=None, height=None, palette=None, x=0, y=0, num_tiles=(1, 1), tile_width=None,
               tile_height=None,
               crop=False, show=None, group=None):
        if width is None:
            width = self.width
        if height is None:
            height = self.height
        palette = self.palette(palette)
        bitmap = displayio.Bitmap(width, height, len(palette))

        w, h = num_tiles
        if tile_width is None:
            tile_width = bitmap.width / w
        if tile_height is None:
            tile_height = bitmap.height / h
        if crop:
            tile_width = int(tile_width)
            height = int(tile_height)
        assert not tile_width % 1, f"width ({width}) must be divisible by number of tiles wide ({w})"
        assert not tile_height % 1, f"height ({height}) must be divisible by number of tiles high ({h})"
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette, x=x, y=y,
                                       width=w, height=h, tile_width=int(tile_width),
                                       tile_height=int(tile_height))
        self.display(tile_grid, show=show, group=group)
        return bitmap, tile_grid

    def circle(self, x0=30, y0=30, r=20, fill='white', outline='white', stroke: int = 1, show=None, group=None):
        from adafruit_display_shapes.circle import Circle
        circle = Circle(x0, y0, r, fill=get_color(fill), outline=get_color(outline), stroke=stroke)
        self.display(circle, show=show, group=group)
        return circle

    def line(self, x0=None, y0=None, x1=None, y1=None, color='white', x=None, y=None, show=None, group=None):
        from adafruit_display_shapes.line import Line
        if x is not None:
            if x0 is None:
                x0 = x
            if x1 is None:
                x1 = x
        if y is not None:
            if y0 is None:
                y0 = 0
            if y1 is None:
                y1 = self.height - 1
        if x0 is None:
            x0 = 0
        if x1 is None:
            x1 = x0
        if y0 is None:
            y0 = 0
        if y1 is None:
            y1 = y0
        line = Line(x0, y0, x1, y1, color=get_color(color))
        self.display(line, show=show, group=group)
        return line

    def path(self, points, color="white", show=None, group=None):
        path = displayio.Group()
        if isinstance(color, (str, int)) or isinstance(color, (list, tuple)) and not (
                len(color) == 3 and all(isinstance(c, int) and 0 <= c <= 255 for c in color)):
            color = [color] * (len(points) - 1)
        assert len(points) > 1, "path must have at least two points"
        assert len(color) == (len(points) - 1), "incorrect number of colors"
        for i, p in enumerate(points[:-1]):
            p2 = points[i + 1]
            self.line(p[0], p[1], p2[0], p2[1], color=color[i], show=True, group=path)
        self.display(group, show=show, group=group)

    def polygon(self, points, outline='white', show=None, group=None):
        from adafruit_display_shapes.polygon import Polygon
        polygon = Polygon(points, outline=get_color(outline))
        self.display(polygon, show=show, group=group)
        return polygon

    def rect(self, x=20, y=20, width=80, height=40, fill='white', outline='white', stroke: int = 1, show=None,
             group=None):
        from adafruit_display_shapes.rect import Rect
        rect = Rect(x, y, width, height, fill=get_color(fill), outline=get_color(outline), stroke=stroke)
        self.display(rect, show=show, group=group)
        return rect

    def round_rect(self, x=20, y=20, width=80, height=40, r=None, fill='white', outline='white', stroke: int = 1,
                   show=None, group=None):
        from adafruit_display_shapes.roundrect import RoundRect
        if r is None:
            r = int(((width + height) / 2) * 0.075)
        round_rect = RoundRect(x, y, width, height, r, fill=get_color(fill), outline=get_color(outline), stroke=stroke)
        self.display(round_rect, show=show, group=group)
        return round_rect

    def sparkline(self, values=(0, 0, 0), width=None, height=None, max_items=None, y_min=None, y_max=None, x=0, y=0,
                  color='white', show=None, group=None):
        from adafruit_display_shapes.sparkline import Sparkline

        if width is None:
            width = self.width
        if height is None:
            height = self.height
        if max_items is None:
            max_items = width
        sparkline = Sparkline(width, height, max_items, y_min=y_min, y_max=y_max, x=x, y=y, color=get_color(color))
        for v in values:
            sparkline.add_value(v, update=False)
        sparkline.update()
        self.display(sparkline, show=show, group=group)
        return sparkline

    def triangle(self, x0: int, y0: int, x1: int, y1: int, x2: int, y2: int, fill=None, outline=None, show=None,
                 group=None):
        from adafruit_display_shapes.triangle import Triangle

        triangle = Triangle(x0, y0, x1, y1, x2, y2, fill=get_color(fill), outline=get_color(outline))
        self.display(triangle, show=show, group=group)
        return triangle

    def image(self, fn, transparent_indices=(0,), show=None, group=None):
        import adafruit_imageload

        image, palette = adafruit_imageload.load(fn, bitmap=displayio.Bitmap, palette=displayio.Palette)
        if transparent_indices is not None:
            for ind in transparent_indices:
                palette.make_transparent(ind)
        tile_grid = displayio.TileGrid(image, pixel_shader=palette, x=0, y=0, tile_width=240, tile_height=240)
        self.display(tile_grid, show=show, group=group)
        return tile_grid

    def text(self, text="Hello World", scale=2, x=50, y=120, color=0xFFFFFF, show=None, group=None, **kwargs):
        from components.display.color_text import ColorText

        text_group = ColorText(text, scale=scale, x=x, y=y, color=color, **kwargs)
        self.display(text_group, show=show, group=group)
        return text_group

    def type(self, text="Hello World", scale=2, x=50, y=120, color=0xFFFFFF, show=None, group=None,
             letter_delay=0.1, word_delay=0.5, line_delay=1, cursor="|", type=True, **kwargs):
        from components.display.color_text import ColorText

        text_group = ColorText("", scale=scale, x=x, y=y, color=color, type=type, letter_delay=letter_delay,
                               word_delay=word_delay, line_delay=line_delay, cursor=cursor, **kwargs)
        self.display(text_group, show=show, group=group)
        text_group.type(text)
        return text_group

    def check(self):
        pass


def test_display():
    d = Display()

    t = d.type("Welcome!\nTyping is COOL\nbut SLOWS DOWN",
               cursor="_", x=20, y=20, letter_delay=0.02, word_delay=0, line_delay=0)
    time.sleep(1)
    d.remove(t)
    del t

    image = d.image("imgs/weargaroo_logo.bmp")
    time.sleep(5)
    d.remove(image)
    del image

    p = d.polygon([(20, 20), (200, 20), (60, 60), (90, 200)])
    time.sleep(5)
    d.remove(p)
    del p

    t = d.text(" Hello World ", color="blue", background_color="white")
    time.sleep(2)

    c = d.circle(fill='red')
    for _ in range(100):
        c.x += 1
        c.y += 1
        time.sleep(0.01)
    d.remove(t)
    del t

    time.sleep(2)
    d.remove(c)
    del c

    r = d.rect(fill='blue')
    for _ in range(100):
        r.x += 1
        r.y += 1
        time.sleep(0.01)
    d.remove(r)
    del r

    s = d.sparkline([4, 20, 3], max_items=7)
    values = [4, 10, 7, 3, 4, 22, 23, 27, 2, 8, 14, 17, 3, 1, 9]
    for v in values:
        time.sleep(0.1)
        s.add_value(v)

    del s

    d.type("That's all\nfor now!", letter_delay=0.05, color="pink")
    time.sleep(10)


if __name__ == "__main__":
    test_display()
