import displayio

from components import Display
from components.display.colors import get_color


class Graph(object):
    def __init__(self, *xy, x=None, y=None, display=None,
                 width=240, height=240, x_min=0, y_min=0, x_max=None, y_max=None,
                color='white', x_color=None, y_color=None,

                title=None, title_scale=3, title_color=None, title_space=None,

                axis_color=None, x_axis_color=None, y_axis_color=None,

                label_space=None, x_label_space=None, y_label_space=None,
                x_label=None, y_label=None,
                label_color=None, x_label_color=None, y_label_color=None,
                label_scale=2, x_label_scale=None, y_label_scale=None,

                tick_interval=None, x_tick_interval=None, y_tick_interval=None,
                tick_length=5, x_tick_length=None, y_tick_length=None,
                tick_offset=2, x_tick_offset=None, y_tick_offset=None,
                tick_color=None, x_tick_color=None, y_tick_color=None,

                grid_interval=None, x_grid_interval=None, y_grid_interval=None,
                grid_color=None, x_grid_color=None, y_grid_color=None,

                tick_label_space=None, x_tick_label_space=None, y_tick_label_space=None,
                tick_label_interval=None, x_tick_label_interval=None, y_tick_label_interval=None,
                tick_label_color=None, x_tick_label_color=None, y_tick_label_color=None,
                tick_label_scale=1, x_tick_label_scale=None, y_tick_label_scale=None,
                ):
        if display is None:
            display = Display()
        self.display = display

        self.data = self.set_data(*xy, x=x, y=y)


        x_axis_color = self.first(x_axis_color, axis_color, x_color, color, 'white')
        y_axis_color = self.first(y_axis_color, axis_color, y_color, color, 'white')
        x_label_color = self.first(x_label_color, label_color, x_color, color, 'white')
        y_label_color = self.first(y_label_color, label_color, y_color, color, 'white')
        x_label = self.first(x_label, "")
        y_label = self.first(y_label, "")
        x_label_scale = self.first(x_label_scale, label_scale)
        y_label_scale = self.first(y_label_scale, label_scale)
        x_label_space = self.first(x_label_space, label_space, 20*x_label_scale)
        y_label_space = self.first(y_label_space, label_space, 20*y_label_scale)
        x_tick_length = self.first(x_tick_length, tick_length, 0)
        y_tick_length = self.first(y_tick_length, tick_length, 0)
        x_tick_offset = self.first(x_tick_offset, tick_offset, 0)
        y_tick_offset = self.first(y_tick_offset, tick_offset, 0)
        x_tick_color = self.first(x_tick_color, tick_color, x_color, color, 'white')
        y_tick_color = self.first(y_tick_color, tick_color, y_color, color, 'white')
        x_tick_label_interval = self.first(x_tick_label_interval, tick_label_interval)
        y_tick_label_interval = self.first(y_tick_label_interval, tick_label_interval)
        x_tick_label_color = self.first(x_tick_label_color, tick_label_color, x_color, color, 'white')
        y_tick_label_color = self.first(y_tick_label_color, tick_label_color, y_color, color, 'white')
        x_tick_label_scale = self.first(x_tick_label_scale, tick_label_scale, x_label_scale, label_scale)
        y_tick_label_scale = self.first(y_tick_label_scale, tick_label_scale, y_label_scale, label_scale)
        x_tick_label_space = self.first(x_tick_label_space, tick_label_space, 20 * x_label_scale)
        y_tick_label_space = self.first(y_tick_label_space, tick_label_space, 20 * y_label_scale)
        x_grid_interval = self.first(x_grid_interval, grid_interval)
        y_grid_interval = self.first(y_grid_interval, grid_interval)
        x_grid_color = self.first(x_grid_color, grid_color, x_color, color, 'white')
        y_grid_color = self.first(y_grid_color, grid_color, y_color, color, 'white')
        title_space = self.first(title_space, title_scale * 20)

        if y_min is None:
            y_min = min(self.data['y']) if self.data['y'] else 0
        if x_min is None:
            x_min = min(self.data['x']) if self.data['x'] else 0

        if y_min == 0:
            y_offset = x_label_space + x_tick_label_space
        else:
            y_offset = 0


        g = self.display.group()


        y_offset = x_label_space + x_tick_label_space
        x_offset = y_label_space + y_tick_label_space

        graph_width = width - x_offset
        graph_height = height - y_offset - title_space

        axes = self.display.group(group=g)

        x_axis = self.display.line(x0=x_offset, x1=x_offset + graph_width - 1, y=y_offset,
                                   color=get_color(x_axis_color), group=axes)

        y_axis = self.display.line(x=x_offset, y0=y_offset, y1=y_offset + graph_height - 1,
                                   color=get_color(y_axis_color), group=axes)


    def set_data(self, *xy, x=None, y=None):
        if len(xy) == 2 and x is None and y is None:
            x, y = xy
        elif len(xy) == 1 and x is None and y is not None:
            x = xy
        elif len(xy) == 1:
            y = xy
        if y is None:
            y = []
        if x is None:
            x = range(len(y))
        x = list(x)
        y = list(y)
        assert len(x) == len(y), "x and y length mismatch"
        self.data = {"x": x, "y": y}
        return self.data

    def first(self, *args):
        for arg in args:
            if arg is not None:
                return arg


    def clip(self, x, y):
        x = min([self.x_max, max([self.x_min, x])])
        y = min([self.y_max, max([self.y_min, y])])
        return x, y

    def locate(self, x, y):
        x, y = self.clip(x, y)
        page_x = int(self.x_scale * (x - self.x_min) + self.left)
        page_y = 240 - int(self.y_scale * (y - self.y_min) + self.bottom)
        return page_x, page_y

    def init(self):
        # create a background
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
            px, py = self.locate(x, y)
            self.display.write_text(str(label), 1, px, px, color=0xFFFFFF)
