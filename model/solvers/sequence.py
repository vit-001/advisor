# -*- coding: utf-8 -*-
__author__ = 'Vit'

from numpy.fft import rfft, rfftfreq
from numpy import abs as np_abs
import math


class Sequence:
    def __init__(self, maximum_lenght):
        self.array = list()
        self.max_lenght = maximum_lenght

    def add(self, value):
        self.array.insert(0, value)
        if len(self.array) > self.max_lenght:
            self.array.pop()

    def fft(self):
        return rfft(self.array)
        pass


if __name__ == "__main__":
    sig = list((
    1.13359, 1.13353, 1.13349, 1.13359, 1.1337, 1.13372, 1.134, 1.13403, 1.13393, 1.13402, 1.13369, 1.13369, 1.13378,
    1.13402, 1.13397, 1.13383, 1.13378, 1.13368, 1.13373, 1.13337, 1.1333, 1.13298, 1.13309, 1.13294, 1.13291, 1.13322,
    1.13306, 1.13285, 1.13283, 1.13294, 1.13304, 1.13343, 1.13322, 1.13324, 1.13336, 1.13339, 1.13304, 1.133, 1.13297,
    1.13289, 1.13301, 1.13301, 1.13304, 1.1328, 1.13251, 1.1323, 1.13232, 1.13234, 1.13203, 1.13232, 1.13229, 1.13228,
    1.13225, 1.13203, 1.13197, 1.13217, 1.13232, 1.13214, 1.132, 1.13203, 1.13205, 1.13225, 1.13225, 1.13248, 1.13249,
    1.1325, 1.13262, 1.13289, 1.13278, 1.13264, 1.13263, 1.13283, 1.13307, 1.13329, 1.1335, 1.13336, 1.13332, 1.13336,
    1.13332, 1.13318, 1.13306, 1.13334, 1.13348, 1.13345, 1.13362, 1.13373, 1.13363, 1.13373, 1.13387, 1.13387, 1.13369,
    1.13373, 1.13384, 1.13423, 1.13438, 1.13439, 1.13445, 1.13456, 1.13448, 1.13445, 1.13463))

    import matplotlib.pyplot as plt


    s = Sequence(100)
    for data in sig:
        s.add(data)

    plt.plot(sig)
    plt.grid(True)
    plt.show()

    sp = (np_abs(s.fft()) / 100).tolist()
    sp.pop(0)

    print(sp)

    plt.plot(rfftfreq(99), sp)
    plt.grid(True)
    plt.show()

