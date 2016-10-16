# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

from model.base_classes import AbstractSolver

class FractalsTradeSignal(AbstractSolver):
    def __init__(self, ma_solver, cs_solver):
        self._ma_solver=ma_solver
        self._cs_solver=cs_solver
        self._delta =  self._ma_solver.delta
        self._ma=list()
        self._cs=list()
        self._signal=0.0
        self._curr_delta=0.0

        self.setting()

        self.fractal_type=None

    def setting(self, ma_period=20):
        self._ma_period=ma_period

    def on_init(self, environment):
        super().on_init(environment)
        self._next_time = self.env.start_time + self._delta

    def on_bid_change(self, time, bid, ask):
        if time >= self._next_time:
            self._ma.insert(0,self._ma_solver.get_lma(self._ma_period))
            if len(self._ma)==4:
                self._ma.pop()

            self._cs.insert(0,self._cs_solver.get_candle())
            if len(self._cs)==4:
                self._cs.pop()


            self._next_time += self._delta

        if self.fractal_type is not None:
            self.calc_signal(bid,ask)

    def on_min_fractal(self,time,value):
        self.fractal_time=time
        self.fractal_value=value
        self.fractal_type='MIN'


        #
        # delta=self._ma[2]-value
        # delta_current=

        # self.signal=self._ma[2]-value

    def calc_signal(self, bid, ask):
        curr_delta=(self._ma_solver.get_lma(self._ma_period)-ask)/(ask-bid)
        self._curr_delta=curr_delta


        # if self._cs[0].low > self._cs[1].low:     # критерий монотонности минимумов - работает на 50%
        # if self._ma[0]> self._ma[1]:              # критерий роста MA - не работает совсем
        if self._cs[0].low > self._cs[1].low and self._cs[0].high > self._cs[1].high:     # критерий монотонности минимумов и максимумов - проверяем

            self._signal=curr_delta
        else:
            self._signal=0.0







        self.fractal_type=None


    @property
    def signal(self):
        signal=self._signal
        self._signal=0.0
        return signal

    @property
    def delta(self):
        delta=self._curr_delta
        self._curr_delta=0.0
        return delta


if __name__ == "__main__":
    pass