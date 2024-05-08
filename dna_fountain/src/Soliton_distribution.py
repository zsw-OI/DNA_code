import math
import random

import numpy as np
class Soliton_distribution(object):
    def __init__(self, K, c, delta):
        self.K = K
        self.delta = delta
        self.c = c
        self.p = [0 for i in range(0, K)]
        self.t =  [0 for i in range(0, K)]
        self.sum =  [0 for i in range(0, K)]
        self.Z = 0
        self.s = c * math.sqrt(K) * (math.log(K / delta))
        if self.s < 1:
            self.s = 1
        self.init()
    def init(self):
        self.p[0] = 1 / self.K
        for i in range(1, self.K):
            self.p[i] = 1 / i / (i + 1)
        l = math.floor(self.K / self.s)
        for i in range(0, min(l, self.K)):
            self.t[i] = self.s / self.K / (i + 1)
        if l < self.K:
            self.t[l] = self.s * math.log(self.s / self.delta) / self.K
        for i in range(0, self.K):
            self.sum[i] = self.p[i] + self.t[i]

        self.sum = np.array(self.sum)
        self.Z = np.sum(self.sum)
        self.sum /= self.Z
        self.sum = np.cumsum(self.sum)
    def calculate(self, seed):
        random.seed(seed)
        x = random.random()
        for i in range(0, self.K):
            if x <= self.sum[i]:
                return i + 1


