# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

from model.base_classes import AbstractSolver

class Fractals(AbstractSolver):
    def __init__(self, candlestick_solver, on_max_found_handler=lambda time,value:None, on_min_found_handler=lambda time,value:None  ):
        self._cs=candlestick_solver
        self._delta = self._cs.delta

        self._max_hdlr=on_max_found_handler
        self._min_hdlr=on_min_found_handler

        self._candle_queue=list()

    def on_init(self, environment):
        super().on_init(environment)
        self._next_time = self.env.start_time + self._delta

    def on_bid_change(self, time, bid, ask):
        if time >= self._next_time:
            candle=self._cs.get_candle()
            self._candle_queue.insert(0,candle)
            if len(self._candle_queue)==6:
                self._candle_queue.pop()

            if self._test_max_of_5():
                # self.old_max=self.local_max
                # self.local_max=self.candle_queue[1].high
                self._max_hdlr(time-self._delta*2, self._candle_queue[2].high)
            # else:
            #     self.local_max=0.0

            if self._test_min_of_5():
                # self.old_min=self.local_min
                # self.local_min=self.candle_queue[1].low
                self._min_hdlr(time-self._delta*2, self._candle_queue[2].low)
            # else:
            #     self.local_min=0.0

            # print(self.candle_queue)

            self._next_time += self._delta

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

    def _test_max_of_3(self):
        if len(self._candle_queue)<3:
            return False
        if self._candle_queue[1].high >= self._candle_queue[0].high and self._candle_queue[1].high >= self._candle_queue[2].high:
            return True
        else:
            return False

    def _test_min_of_3(self):
        if len(self._candle_queue)<3:
            return False
        if self._candle_queue[1].low <= self._candle_queue[0].low and self._candle_queue[1].low <= self._candle_queue[2].low:
            return True
        else:
            return False

if __name__ == "__main__":
    pass