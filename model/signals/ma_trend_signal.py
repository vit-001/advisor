# -*- coding: utf-8 -*-
__author__ = 'Vit'

from model.base_classes import AbstractSolver
from model.solvers.moving_average_array import MovindAverageSimpleArray

class MATrendSignal(AbstractSolver):
    def __init__(self, candlestick_solver, ma_solver, depth_of_ma_in_period):
        self._css=candlestick_solver
        self._mas=ma_solver
        self._ap=depth_of_ma_in_period
        # self.buy_signal=0.0
        # self.sell_signal=0.0

        self.mats_buy_array = MovindAverageSimpleArray(12)
        self.mats_sell_array = MovindAverageSimpleArray(12)

    # def on_bid_change(self, time, bid, ask):
    #     candle=self._css.get_candle()

    def on_init(self, environment):
        super().on_init(environment)
        self.next_time = self.env.start_time + self._mas.delta

    def on_bid_change(self, time, bid, ask):
        if time >= self.next_time:
            self.mats_buy_array.on_change(self.buy_signal(self._ap))
            self.mats_sell_array.on_change(self.sell_signal(self._ap))
            self.next_time += self._mas.delta

    def buy_signal(self, depth_of_ma_in_period):
        candle=self._css.get_candle()
        ma=self._mas.get_lma(depth_of_ma_in_period)

        if candle.low > ma:
            return 1.0
        else:
            if candle.high < ma:
                self.mats_buy_array = MovindAverageSimpleArray(60)
                return -1.0
        return 0.0

    def sell_signal(self, depth_of_ma_in_period):
        candle=self._css.get_candle()
        ma=self._mas.get_lma(depth_of_ma_in_period)

        if candle.high < ma:
            return 1.0
        else:
            if candle.low > ma:
                self.mats_sell_array = MovindAverageSimpleArray(60)
                return -1.0
        return 0.0

    @property
    def average_buy_signal(self):
        return self.mats_buy_array.get_lma(10)

    @property
    def average_sell_signal(self):
        return self.mats_sell_array.get_lma(10)

if __name__ == "__main__":
    pass