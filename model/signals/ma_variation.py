# -*- coding: utf-8 -*-
__author__ = 'Vit'

from model.base_classes import AbstractSolver
from model.solvers.moving_average_array import MovindAverageSimpleArray

class MomentumMA(AbstractSolver):
    def __init__(self, ma_solver, ma_period, dimension):
        self._ma=ma_solver
        self._delta=ma_solver.delta
        self._ma_period=ma_period

        self.ma_array=MovindAverageSimpleArray(dimension)
        # self.ma_momentum_array=MovindAverageSimpleArray(dimension)
        self.n=0

    def on_init(self, environment):
        super().on_init(environment)
        self._next_time = self.env.start_time + self._delta

    def on_bid_change(self, time, bid, ask):
        if time >= self._next_time:
            new_ma=self._ma.get_lma(self._ma_period)
            self.ma_array.on_change(new_ma)

            self.n +=1
            self._next_time += self._delta

    def get_momentum_lma(self, time_shift):
        if time_shift >= self.n:
            return 0.0
        return self.ma_array.get_past_value(0)-self.ma_array.get_past_value(time_shift)



if __name__ == "__main__":
    pass