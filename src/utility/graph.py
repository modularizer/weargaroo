import displayio
from components.display import Display


class Graph(object):
    def __init__(self, color_palette, x_min=0, x_max=200, y_min=-1, y_max=1, top=20, bottom=220, left=20, right=220,
                 x_ticks=(), y_ticks=(), labels=()):
        self.color_palette = color_palette
        self.height = bottom - top
        self.width = right - left
        self.x_range = x_max - x_min
        self.y_range = y_max - y_min
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.x_scale = self.width / self.x_range
        self.y_scale = self.height / self.y_range
        self.x_ticks = x_ticks
        self.y_ticks = y_ticks
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        self.labels = labels
        self.display = Display()
        self.bitmap = self.clear()

    def clip(self, x, y):
        x = min([self.x_max, max([self.x_min, x])])
        y = min([self.y_max, max([self.y_min, y])])
        return x, y

    def locate(self, x, y):
        x, y = self.clip(x, y)
        page_x = int(self.x_scale * (x - self.x_min) + self.left)
        page_y = 240 - int(self.y_scale * (y - self.y_min) + self.bottom)
        return page_x, page_y

    def clear(self):
        self.display.clear()
        self.bitmap = self.display.init_bitmap()
        return self.bitmap

    def init(self, color_palette):
        # create a background
        splash, tile_grid, bitmap = color_palette.splash()

        for tick in self.x_ticks:
            if isinstance(tick, int):
                tick = (tick,)
            x = tick[0]
            if len(tick) == 1:
                start = self.y_min
                stop = self.y_max
                step = 1
            elif len(tick) == 2:
                start = self.y_min
                stop = tick[1]
                step = 1
            elif len(tick) == 3:
                start = tick[1]
                stop = tick[2]
                step = 1
            elif len(tick) == 4:
                start = tick[1]
                stop = tick[2]
                step = tick[3]
            page_start, page_stop = self.locate(start, stop)
            for y in range(page_start, page_stop + 1, step):
                self.bitmap[x][y] = 1

        for tick in self.x_ticks:
            if isinstance(tick, int):
                tick = (tick,)
            y = tick[0]
            if len(tick) == 1:
                start = self.x_min
                stop = self.x_max
                step = 1
            elif len(tick) == 2:
                start = self.x_min
                stop = tick[1]
                step = 1
            elif len(tick) == 3:
                start = tick[1]
                stop = tick[2]
                step = 1
            elif len(tick) == 4:
                start = tick[1]
                stop = tick[2]
                step = tick[3]
            for x in range(start, stop + 1, step):
                self.bitmap[x][y] = 1

        for label, (x, y) in self.labels.items():
            px, py




        global bitmap
        bitmap = display.init_bitmap()

        def on_value(ind, value, dv, phase, new_phase):
            global bitmap
            print(value, dv)
            # y = max([0, min([239, 120 - int(200 * dv)])])
            y = max([0, min([239, 120 - int(100 * value)])])
            bitmap[ind % 240, y] = 1
            if not (ind % 240):
                display.clear()
                display.write_text(str(p.rate), 2, 40, 200, color=0xFFFFFF)
                time.sleep(0.5)
                display.clear()
                bitmap = display.init_bitmap()
                for x in range(240):
                    bitmap[x, 80] = 1
                    bitmap[x, 120] = 1
                    bitmap[x, 160] = 1