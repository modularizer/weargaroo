class Colors(object):
    white = 0xffffff
    black = 0

    red = 0xff0000
    green = 0x00ff00
    blue = 0x0000ff

    yellow = 0xffff00
    pink = 0xff00ff
    cyan = 0x00ffff

    gray = 0x808080
    dark_red = 0x800000
    dark_green = 0x008000
    dark_blue = 0x000080

    dark_yellow = 0x808000
    dark_pink = 0x800080
    dark_cyan = 0x008080

    purple = dark_pink
    navy = dark_blue
    turquoise = dark_cyan

    def dict(self):
        d = {k: getattr(self, k) for k in dir(self) if not k.startswith('_')}
        return {k: v for k, v in d.items() if isinstance(v, int)}

    def to_rgb(self, value):
        r = value >> 16
        g = (value >> 8) % (1 << 8)
        b = value % (1 << 8)
        return r, g, b

    def color_diff(self, a, b):
        ra, ga, ba = self.to_rgb(a)
        rb, gb, bb = self.to_rgb(b)
        dr = ra - rb
        dg = ga - gb
        db = ba - bb
        return (dr ** 2 + dg ** 2 + db ** 2) ** 0.5

    def color_search(self, value):
        for k, v in self.dict().items():
            if v == value:
                return k
        return self.closest_color(value)

    def closest_color(self, value):
        min_error = 255
        closest_color = "unknown"
        for k, v in self.dict().items():
            e = self.color_diff(value, v)
            if e < min_error:
                closest_color = k
            if not e:
                return k
        return closest_color