# -*- coding: utf-8 -*-
__author__ = 'Vit'

from model.base_classes import AbstractSolver
from model.solvers.moving_average_array import MovindAverageSimpleArray

class Point:
    def __init__(self, time, value):
        self.time=time
        self.value=value

class Fractals(AbstractSolver):
    def __init__(self, candlestick_solver, dimension):
        self._cs=candlestick_solver
        self.delta = self._cs.delta

        self.candle_queue=list()

        self.max_arr=list()
        self.min_arr=list()

        self.local_max=0.0
        self.local_min=0.0

        self.old_max=0.0
        self.old_min=0.0


    def on_init(self, environment):
        super().on_init(environment)
        self.next_time = self.env.start_time + self.delta

    def on_bid_change(self, time, bid, ask):
        if time >= self.next_time:
            candle=self._cs.get_candle()
            self.candle_queue.insert(0,candle)
            if len(self.candle_queue)==6:
                self.candle_queue.pop()

            if self._test_max_of_3():
                self.old_max=self.local_max
                self.local_max=self.candle_queue[1].high
            # else:
            #     self.local_max=0.0

            if self._test_min_of_3():
                self.old_min=self.local_min
                self.local_min=self.candle_queue[1].low
            # else:
            #     self.local_min=0.0

            # print(self.candle_queue)

            self.next_time += self.delta

    def max_ind(self):
        return self.local_max-self.old_max

    def min_ind(self):
        return self.local_min-self.old_min

    def _test_max_of_3(self):
        if len(self.candle_queue)<3:
            return False
        if self.candle_queue[1].high > self.candle_queue[0].high and self.candle_queue[1].high > self.candle_queue[2].high:
            return True
        else:
            return False

    def _test_min_of_3(self):
        if len(self.candle_queue)<3:
            return False
        if self.candle_queue[1].low < self.candle_queue[0].low and self.candle_queue[1].low < self.candle_queue[2].low:
            return True
        else:
            return False

if __name__ == "__main__":
    pass