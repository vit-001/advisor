# -*- coding: utf-8 -*-
__author__ = 'Vit'

from model.solvers.moving_average_array import MovindAverageSimpleArray
from model.base_classes import AbstractSolver

class MovingAverage(AbstractSolver):
    def __init__(self, candle_solver, dimension):
        self._cs=candle_solver

        self.close=MovindAverageSimpleArray(dimension)
        self.open=MovindAverageSimpleArray(dimension)
        self.high=MovindAverageSimpleArray(dimension)
        self.low=MovindAverageSimpleArray(dimension)
        self.median=MovindAverageSimpleArray(dimension)
        self.typical=MovindAverageSimpleArray(dimension)
        self.weighted_close=MovindAverageSimpleArray(dimension)

        self._cs.add_handler(self.on_candle)

    def on_candle(self,time,candle):
        self.close.on_change(candle.close)
        self.open.on_change(candle.open)
        self.high.on_change(candle.high)
        self.low.on_change(candle.low)
        self.median.on_change((candle.high+candle.low)/2.0)
        self.typical.on_change((candle.high+candle.low+candle.close)/3.0)
        self.weighted_close.on_change((candle.high+candle.low+candle.close*2.0)/4.0)

if __name__ == "__main__":
    pass
