# -*- coding: utf-8 -*-
__author__ = 'Vit'

from datetime import datetime


class Tick:
    count = 0
    last_time = datetime(1970, 1, 1)

    def __init__(self, tick_string=""):
        self.number = Tick.count
        Tick.count += 1

        split = tick_string.split(";")
        self.time = datetime.strptime(split[0], "%Y.%m.%d %H:%M:%S")
        if self.time < Tick.last_time:
            raise RuntimeError(tick_string + 'Нарушена временная последовательность выдачи тиков')
        Tick.last_time = self.time
        self.bid = float(split[1])
        self.ask = float(split[2])
        self.last = float(split[3])
        self.volume = int(split[4])
        self.flags = int(split[5])

    def __repr__(self):
        str = "{0:06} {1} {2} {3} {4} {5}".format(self.number, self.time.isoformat(sep=" "), self.bid, self.ask,
                                                  self.last, self.flags)
        return str

    def __str__(self):
        return self.__repr__()


if __name__ == "__main__":
    print("Tick test")
    new_tick = Tick("2016.06.17 00:36 1.12254 1.12273 0.00000 0 96")
    print(new_tick)
    new_tick = Tick("2016.06.17 00:36 1.12254 1.12273 0.00000 0 96")
    print(new_tick)
    new_tick = Tick("2016.06.17 00:36 1.12254 1.12273 0.00000 0 96")
    print(new_tick)
    new_tick = Tick("2016.06.17 00:36 1.12254 1.12273 0.00000 0 96")
    print(new_tick)
