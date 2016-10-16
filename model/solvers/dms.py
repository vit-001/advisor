# -*- coding: utf-8 -*-
__author__ = 'Vit'

from datetime import timedelta

from model.base_classes import AbstractSolver
from model.solvers.moving_average_array import MovindAverageSimpleArray

class DMS(AbstractSolver):
    def __init__(self, candlestick_solver, dimension):
        self._cs=candlestick_solver
        self.delta = self._cs.delta
        self.dimension = dimension

        self.atr_array = MovindAverageSimpleArray(dimension)  # Average true range
        self.pdi_array = MovindAverageSimpleArray(dimension)  # positive directional indicator
        self.ndi_array = MovindAverageSimpleArray(dimension)  # negative directional indicator
        self.adx_array = MovindAverageSimpleArray(dimension)  # average directional movement index

    def on_init(self, environment):
        super().on_init(environment)
        self.next_time = self.env.start_time + self.delta

        self._old_candle=self._cs.get_candle()
        self._old_pdm=0.0
        self._old_ndm=0.0
        self._tr=0.0

    def on_bid_change(self, time, bid, ask):
        if time >= self.next_time:
            new_candle=self._cs.get_candle()

            # рассчитываем True Range
            self._tr=max(new_candle.high,self._old_candle.close)-min(new_candle.low,self._old_candle.close)
            self.atr_array.on_change(self._tr)

            # рассчитываеи +-DM
            pdm = 0.0  # значение +DM
            ndm = 0.0  # значение -DM

            pm = new_candle.high - self._old_candle.high  # изменение максимума
            if pm < 0.0:
                pm = 0.0
            nm = self._old_candle.low - new_candle.low  # изменение минимума
            if nm < 0.0:
                nm = 0.0
            if pm != nm:
                if pm > nm:  # выбираем наибольшее изменение
                    pdm = pm
                else:
                    ndm = nm

            # рассчитываем +-DI
            if self._tr > 0.0:
                self.pdi_array.on_change(pdm / self._tr)
                self.ndi_array.on_change(ndm / self._tr)

            # рассчитываем ADX
            self.adx_array.on_change(self.get_dxi(14)) #todo решить, какое здесь число ставить

            self._old_ndm=ndm
            self._old_pdm=pdm
            self._old_candle=new_candle
            self.next_time += self.delta

    def get_tr(self):
        return self._tr

    def get_atr(self, period):
        return self.atr_array.get_ma(period)

    def get_atr_linear(self, period):
        return self.atr_array.get_lma(period)

    def get_atr_exp(self, period):
        return self.atr_array.get_ema(period)

    def get_pdm(self):
        return self._old_pdm

    def get_ndm(self):
        return self._old_ndm

    def get_pdi(self, period):
        return self.pdi_array.get_ema(period)

    def get_ndi(self, period):
        return self.ndi_array.get_ema(period)

    def get_dxi(self, period):
        pdi=self.get_pdi(period)
        ndi=self.get_ndi(period)
        if pdi+ndi==0.0:
            return 0.0

        return abs(pdi-ndi)/(pdi+ndi)

    def get_adxi(self, period):
        return self.adx_array.get_ma(period)


if __name__ == "__main__":
    pass



