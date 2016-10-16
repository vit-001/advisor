# -*- coding: utf-8 -*-
__author__ = 'Vit'

from datetime import timedelta

from model.base_classes import AbstractSolver
from model.solvers.moving_average_array import MovindAverageSimpleArray


class TRquantum:
    def __init__(self):
        self.min = 0.0
        self.max = 0.0
        self.valid = False

    def add(self, value):
        if self.valid:
            self.min = min(self.min, value)
            self.max = max(self.max, value)
        else:
            self.min = value
            self.max = value
            self.valid = True

    @property
    def value(self):
        if self.valid:
            return self.max - self.min
        raise RuntimeError("Неинициализированное значение TRquantum")

    def __repr__(self):
        return 'TR:{0:.6f}'.format(self.value)


class DMquantum:
    def __init__(self, old_min, old_max, first_time_run=False):
        self.first_time_run = first_time_run
        self.old_min = old_min
        self.old_max = old_max
        self.curr_min = None
        self.curr_max = None

    def add(self, value):
        if self.first_time_run:
            self.old_max = value
            self.old_min = value
            self.first_time_run = False

        if self.curr_max is None:
            self.curr_max = value
            self.curr_min = value
        else:
            self.curr_max = max(self.curr_max, value)
            self.curr_min = min(self.curr_min, value)

    @property
    def value(self):
        pdm = 0.0  # значение +DM
        ndm = 0.0  # значение -DM

        if not (self.curr_max is None or self.curr_max is None):

            pm = self.curr_max - self.old_max  # изменение максимума
            # print(pm, end=', ')
            if pm < 0.0:
                pm = 0.0
            nm = self.old_min - self.curr_min  # изменение минимума
            # print(nm)
            if nm < 0.0:
                nm = 0.0
            if pm == nm:
                return (pdm, ndm)  # возвращаем (0,0)

            if pm > nm:  # выбираем наибольшее изменение
                pdm = pm
            else:
                ndm = nm

        return (pdm, ndm)  # возвращаем (+DM,-DM)

    def test_print(self):
        print(self.old_min, self.old_max, '  ', self.curr_min, self.curr_max)


class DMSOld(AbstractSolver):
    def __init__(self, quantum_in_sec, dimension):
        self.delta = timedelta(seconds=quantum_in_sec)
        self.dimension = dimension

        self.current_tr = TRquantum()
        self.last_tr = TRquantum()
        self.prev_bid = 0.0

        self.current_dm = DMquantum(0.0, 0.0, True)
        self.last_dm = DMquantum(0.0, 0.0, True)

        self.atr_array = MovindAverageSimpleArray(dimension)  # Average true range
        self.pdi_array = MovindAverageSimpleArray(dimension)  # positive directional indicator
        self.ndi_array = MovindAverageSimpleArray(dimension)  # negative directional indicator
        self.adx_array = MovindAverageSimpleArray(dimension)  # average directional movement index

    def on_init(self, environment):
        super().on_init(environment)
        self.next_time = self.env.start_time + self.delta

    def on_bid_change(self, time, bid, ask):
        # print(bid)
        if time >= self.next_time:
            # только здесь правильное значение TR, +-DM
            try:
                tr = self.current_tr.value
            except RuntimeError:
                tr=0.0
            self.atr_array.on_change(tr)
            dm = self.current_dm.value
            if tr > 0.0:
                self.pdi_array.on_change(dm[0] / tr)
                self.ndi_array.on_change(dm[1] / tr)

            self.adx_array.on_change(self.get_dxi(14)) #todo решить, какое здесь число ставить

            self.last_tr = self.current_tr
            self.current_tr = TRquantum()
            self.current_tr.add(self.prev_bid)

            self.last_dm=self.current_dm
            self.current_dm=DMquantum(self.last_dm.curr_min,self.last_dm.curr_max)

            self.next_time += self.delta

        self.current_tr.add(bid)
        self.current_dm.add(bid)
        self.prev_bid = bid

    def get_tr(self):
        return self.last_tr.value

    def get_atr(self, period):
        return self.atr_array.get_ma(period)

    def get_atr_linear(self, period):
        return self.atr_array.get_lma(period)

    def get_pdm(self):
        return self.last_dm.value[0]

    def get_ndm(self):
        return self.last_dm.value[1]

    def get_pdi(self, period):
        return self.pdi_array.get_lma(period)

    def get_ndi(self, period):
        return self.ndi_array.get_lma(period)

    def get_dxi(self, period):
        pdi=self.get_pdi(period)
        ndi=self.get_ndi(period)
        if pdi+ndi==0.0:
            return 0.0

        return abs(pdi-ndi)/(pdi+ndi)

    def get_adxi(self, period):
        return self.adx_array.get_lma(period)


if __name__ == "__main__":
    pass



