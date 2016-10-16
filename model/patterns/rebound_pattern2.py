# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

from model.base_classes import AbstractSolver
from model.solvers.moving_average_cs import MovingAverage
from datetime import timedelta

class ReboundPatternSignal(AbstractSolver): #todo
    def __init__(self, cs_m1_solver):
        self._cs=cs_m1_solver
        self._ma=MovingAverage(self._cs,200)

        self._current_candle_time=None
        self._current_candle=None

        self._candle_queue=list()
        self._ma_queue=list()

        self._buy_signal=0.0
        self._curr_buy_delta=0.0

        self.setting()
        self.set_on_pattern_found_handlers()
        self.set_on_signal_handler()
        self.set_plot_signal_proc()
        self._cs.add_handler(self.on_m1_candle)

    def setting(self,base_period=10, start_minute=3, ma_period=14):
        self._ma_period=ma_period
        self._base_period=base_period
        self._start_minute=start_minute

        self._delta=timedelta(minutes=base_period)

    def set_on_signal_handler(self, handler=lambda:None):
        self._signal_handler=handler

    def set_on_candle_handler(self, handler=lambda time,candle:None):
        self._candle_handler=handler

    def set_on_pattern_found_handlers(self,on_high_found=lambda time,value:None,on_low_found=lambda time,value:None):
        self._high_hdlr=on_high_found
        self._low_hdlr=on_low_found

    def set_plot_signal_proc(self,proc=lambda time,value:None):
        self._plot=proc

    def on_m1_candle(self,candle_time,candle):
        if self._current_candle is None:
            self._current_candle_time=candle_time
            self._current_candle=candle
        else:
            self._current_candle.add_candle(candle)

        time=candle_time.time()
        if (time.hour*60+time.minute)%self._base_period == self._start_minute:
            # print(time.hour,time.minute,time.hour*24+time.minute,self._start_minute)
            # print('RP2',self._current_candle)
            self._candle_handler(candle_time,self._current_candle)
            self._candle_queue.insert(0,self._current_candle)
            if len(self._candle_queue)==16:
                self._candle_queue.pop()

            if self._test_max_of_4():
                self._high_hdlr(candle_time-self._delta*2, self._candle_queue[2].high)
                spread=candle.last_spread
                if spread<0.00001:
                    spread=0.00001

                # print(spread,self._ma.median.get_lma(self._ma_period*self._base_period) )
                curr_delta=(self._ma.median.get_lma(self._ma_period*self._base_period)-self._current_candle.close)/spread
                print(curr_delta)

            if self._test_min_of_4():
                self._low_hdlr(candle_time-self._delta, self._candle_queue[1].low)
                spread=candle.last_spread
                if spread<0.00001:
                    spread=0.00001

                # print(spread,self._ma.median.get_lma(self._ma_period*self._base_period) )
                curr_delta=(self._ma.median.get_lma(self._ma_period*self._base_period)-self._current_candle.close)/spread

                self._curr_buy_delta=curr_delta
                # if self._candle_queue[0].low > self._candle_queue[1].low and self._candle_queue[0].high > self._candle_queue[1].high:     # критерий монотонности минимумов и максимумов - проверяем
                self._buy_signal=curr_delta
                # else:
                #     self._buy_signal=0.0
                self._plot(candle_time,self._buy_signal)
                self._signal_handler()

            else:
                self._plot(candle_time,0.0)

            self._current_candle=None

    @property
    def buy_signal(self):
        # print('bs2=',self._buy_signal)
        signal=self._buy_signal
        self._buy_signal=0.0
        return signal

    @property
    def buy_delta(self):
        delta=self._curr_buy_delta
        self._curr_buy_delta=0.0
        return delta


    def _test_max_of_5(self):
        if len(self._candle_queue)<5:
            return False
        if (self._candle_queue[2].high >= self._candle_queue[0].high and self._candle_queue[2].high >= self._candle_queue[1].high and
            self._candle_queue[2].high >= self._candle_queue[3].high and self._candle_queue[2].high >= self._candle_queue[4].high):
            return True
        else:
            return False

    def _test_min_of_5(self):
        if len(self._candle_queue)<5:
            return False
        if (self._candle_queue[2].low <= self._candle_queue[0].low and self._candle_queue[2].low <= self._candle_queue[1].low and
            self._candle_queue[2].low <= self._candle_queue[3].low and self._candle_queue[2].low <= self._candle_queue[4].low):
            return True
        else:
            return False

    def _test_min_of_4(self):
        if len(self._candle_queue)<5:
            return False
        if (self._candle_queue[1].low <= self._candle_queue[0].low and self._candle_queue[1].low <= self._candle_queue[2].low and
            self._candle_queue[1].low <= self._candle_queue[3].low):
            return True
        else:
            return False

    def _test_max_of_4(self):
        if len(self._candle_queue)<5:
            return False
        if (self._candle_queue[1].high >= self._candle_queue[0].high and self._candle_queue[1].high >= self._candle_queue[2].high and
            self._candle_queue[1].high >= self._candle_queue[3].high):
            return True
        else:
            return False


    def _test_min_of_7(self):
        if len(self._candle_queue)<7:
            return False

        _min=self._candle_queue[2].low
        _min_before=min(self._candle_queue[6].low,self._candle_queue[5].low,self._candle_queue[4].low,self._candle_queue[3].low)
        _min_after=min(self._candle_queue[0].low,self._candle_queue[1].low)

        if _min<=_min_before and _min<=_min_after:
            return True
        else:
            return False


if __name__ == "__main__":
    pass