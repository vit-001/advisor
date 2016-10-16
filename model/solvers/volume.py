# -*- coding: utf-8 -*-
__author__ = 'Nikitin'
from datetime import timedelta

from model.base_classes import AbstractSolver
from model.solvers.moving_average_array import MovindAverageSimpleArray

class VolumeSolver(AbstractSolver):
    def __init__(self, quantum_in_sec, dimension):
        self.delta = timedelta(seconds=quantum_in_sec)
        self.dimension = dimension

        self.current_volume=0
        self.last_volume=0
        self.volume_array = MovindAverageSimpleArray(dimension)  # Average volume

    def on_init(self, environment):
        super().on_init(environment)
        self.next_time = self.env.start_time + self.delta

    def on_bid_change(self, time, bid, ask):

        if time >= self.next_time:
            # только здесь правильное значение volume

            self.volume_array.on_change(float(self.current_volume))
            self.last_volume=self.current_volume
            self.current_volume=0

            self.next_time += self.delta

        self.current_volume += 1

    @property
    def volume(self):
        return self.last_volume

    def get_volume_average(self, period):
        return self.volume_array.get_lma(period)

if __name__ == "__main__":
    pass