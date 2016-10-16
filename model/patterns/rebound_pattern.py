# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

from model.base_classes import AbstractSolver

class ReboundPatternSignal(AbstractSolver):
    def __init__(self, ma_solver, cs_solver):
        self._ma=ma_solver
        self._cs=cs_solver
        self._delta =  self._ma.delta

        self._candle_queue=list()
        self._ma_queue=list()

        self._buy_signal=0.0
        self._curr_buy_delta=0.0

        self.setting()
        self.set_on_pattern_found_handlers()

    def setting(self, ma_period=14):
        self._ma_period=ma_period

    def set_on_pattern_found_handlers(self,on_high_found=lambda time,value:None,on_low_found=lambda time,value:None):
        self._high_hdlr=on_high_found
        self._low_hdlr=on_low_found


    def on_init(self, environment):
        super().on_init(environment)
        self._next_time = self.env.start_time + self._delta


    def on_bid_change(self, time, bid, ask):
        if time >= self._next_time:

            self._candle_queue.insert(0,self._cs.get_candle())
            if len(self._candle_queue)==16:
                self._candle_queue.pop()

            self._ma_queue.insert(0,self._ma.get_lma(self._ma_period))
            if len(self._ma_queue)==16:
                self._ma_queue.pop()

            if self._test_max_of_5():
                self._high_hdlr(time-self._delta*2, self._candle_queue[2].high)
            #
            # if self._test_min_of_5():
            #     self._low_hdlr(time-self._delta*2, self._candle_queue[2].low)
            #
            #     curr_delta=(self._ma.get_lma(self._ma_period)-ask)/(ask-bid)
            #     self._curr_buy_delta=curr_delta
            #     if self._candle_queue[0].low > self._candle_queue[1].low and self._candle_queue[0].high > self._candle_queue[1].high:     # критерий монотонности минимумов и максимумов - проверяем
            #         self._buy_signal=curr_delta
            #     else:
            #         self._buy_signal=0.0

            if self._test_min_of_4():
                self._low_hdlr(time-self._delta, self._candle_queue[1].low)
                spread=ask-bid
                if spread>0.000001:
                    curr_delta=(self._ma.get_lma(self._ma_period)-ask)/spread
                else:
                    curr_delta=(self._ma.get_lma(self._ma_period)-ask)/0.000001
                self._curr_buy_delta=curr_delta
                # if self._candle_queue[0].low > self._candle_queue[1].low and self._candle_queue[0].high > self._candle_queue[1].high:     # критерий монотонности минимумов и максимумов - проверяем
                self._buy_signal=curr_delta
                # else:
                #     self._buy_signal=0.0


            self._next_time += self._delta

    @property
    def buy_signal(self):
        # print('bs =',self._buy_signal)
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