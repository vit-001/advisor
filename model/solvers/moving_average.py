# -*- coding: utf-8 -*-
__author__ = 'Vit'

from datetime import timedelta

from model.solvers.moving_average_array import MovindAverageArray
from model.base_classes import AbstractSolver


class MovingAverage(AbstractSolver):
    def __init__(self, quantum_in_sec, dimension):
        self.array = MovindAverageArray(quantum_in_sec, dimension)
        self.delta = timedelta(seconds=quantum_in_sec)

    def on_init(self, environment):
        super().on_init(environment)
        self.array.on_init(self.env.start_time)

    def on_bid_change(self, time, bid, ask):
        self.array.on_change(time, bid)

    def get_ma(self, duration_in_quantum):
        return self.array.get_ma(duration_in_quantum)

    def get_lma(self, duration_in_quantum):
        return self.array.get_lma(duration_in_quantum)


if __name__ == "__main__":
    pass
