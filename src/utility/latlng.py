
class LatOrLng(object):
    def __init__(self, s):
        a, b = s.split(".")
        self.i = int(a[:-2])
        self.f = int(a[-2:]) / 60 + float("0." + b) / 60
        self.value = self.i + self.f
        self.s = s

    def __float__(self):
        return self.i + self.f

    def __str__(self):
        return str(self.i) + "." +  str(self.f).split(".")[1]

    def __sub__(self, other):
        return float(other) - self.f - float(self.i)
