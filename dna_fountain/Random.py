class Random(object):
    def __init__(self, seed = 1):
        self.num = seed
        self.mask = 0b101000110000000000000000000000001
    def next(self):
        self.num <<= 1
        if (self.num >> 32) != 0:
            self.num ^= self.mask
        return self.num

