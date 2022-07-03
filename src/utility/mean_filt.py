class MeanFilt(object):
    def __init__(self, n=10):
        self.n = n
        self.values = []
        self.length = 0
        self.sum = 0
        self.max = -1e30
        self.min = 1e30

    @property
    def mean(self):
        return self.sum / self.length

    def append(self, val):
        self.values = [val] + self.values
        self.length += 1
        self.sum += val

        # adjust max
        if val > self.max:
            self.max = val
        if val < self.min:
            self.min = val

        while self.length > self.n:
            v = self.values.pop()
            if v == self.max:
                self.max = max(self.values)
            if v == self.min:
                self.min = min(self.values)
            self.sum -= v
            self.length -= 1
