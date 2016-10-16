# -*- coding: utf-8 -*-
__author__ = 'Vit'
from model.base_classes import AbstractSolver
from model.solvers.moving_average_array import MovindAverageSimpleArray

class MACD(AbstractSolver):
    def __init__(self, moving_average_solver, short_period, long_period, average_period):
        self.ma_solver=moving_average_solver
        self.short_period=short_period
        self.long_period=long_period
        self.average_period=average_period

        self.delta=moving_average_solver.delta

        self.macd_array = MovindAverageSimpleArray(average_period)  # Average volume

    def on_init(self, environment):
        super().on_init(environment)
        self.next_time = self.env.start_time + self.delta

    def on_bid_change(self, time, bid, ask):
        if time >= self.next_time:
            self.macd_array.on_change(self.macd)
            self.next_time += self.delta

    @property
    def macd(self):
        try:
            return self.ma_solver.get_lma(self.short_period)-self.ma_solver.get_lma(self.long_period)
        except RuntimeError:
            return 0.0

    @property
    def signal(self):
        return self.macd_array.get_lma(self.average_period)

if __name__ == "__main__":
    pass