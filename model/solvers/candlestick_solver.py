# -*- coding: utf-8 -*-
__author__ = 'Vit'
from datetime import timedelta,datetime

from model.base_classes import AbstractSolver


class Candlestick:
    def __init__(self, open, valid=True):
        # self.time=time
        self.open = open
        self.close = open
        self.high = open
        self.low = open
        self.valid = valid
        self.spread=0.0
        self.last_spread=0.0


    def add(self, bid, ask):
        if self.valid:
            self.close = bid
            if bid < self.low:
                self.low = bid
            if bid > self.high:
                self.high = bid
        else:
            self.open = bid
            self.close = bid
            self.high = bid
            self.low = bid
            self.valid = True

        self.spread=max(self.spread, ask-bid)
        self.last_spread=ask-bid

    def add_candle(self,candle):
        if self.valid:
            self.close=candle.close
            self.high=max(self.high,candle.high)
            self.low=min(self.low,candle.low)
        else:
            self.open=candle.open
            self.close=candle.close
            self.low=candle.low
            self.high=candle.high
            self.valid=True
        self.spread=max(self.spread, candle.spread)
        self.last_spread=candle.last_spread


    def print(self):
        if self.valid:
            print("CS:", self.open, self.high, self.low, self.close)
        else:
            print("Invalid candlestick")

    def csv_format(self):
        return "{0}; {1}; {2}; {3}; ".format(self.open, self.high, self.low, self.close).replace('.', ',')

    def __repr__(self):
        return "CS({0} {1} {2} {3})".format(self.open, self.high, self.low, self.close).replace('.', ',')


class CandlestickSolver(AbstractSolver):
    def __init__(self, period_in_sec):
        self.delta = timedelta(seconds=period_in_sec)
        self.old_candle = Candlestick(0.0, False)
        self.candle_time=datetime(1970,1,1)
        self._handler_list=list()

    def add_handler(self, handler=lambda time,candle: None):
        self._handler_list.append(handler)

    def on_init(self, environment):
        super().on_init(environment)
        self.next_time = self.env.start_time + self.delta
        self.candle = Candlestick(0.0, False)

    def on_bid_change(self, time, bid, ask):
        # print(time,bid)
        if time < self.next_time:
            self.candle.add(bid, ask)
        else:
            self.old_candle = self.candle
            self.candle_time=self.next_time
            self.candle = Candlestick(bid)
            self.next_time += self.delta
            for handler in self._handler_list:
                handler(time, self.old_candle)

    def get_candle(self):
        return self.old_candle

#
# class CandlestickSolverWithHandler(AbstractSolver):
#     def __init__(self, period_in_sec, handler=(lambda candle, time: None)):
#         self.delta = timedelta(seconds=period_in_sec)
#         self.handler = handler
#
#     def on_init(self, environment):
#         super().on_init(environment)
#         self.next_time = self.env.start_time + self.delta
#         self.candle = Candlestick(0.0, False)
#
#     def on_bid_change(self, time, bid, ask):
#         # print(time,bid)
#         if time < self.next_time:
#             self.candle.add(bid, ask)
#         else:
#             if self.candle.valid:
#                 self.handler(self.candle, self.next_time)
#             self.candle = Candlestick(bid)
#             self.next_time += self.delta
#
#
# class CandlestickSolverOnDemand(AbstractSolver):
#     def __init__(self):
#         pass
#
#     def on_init(self, environment):
#         super().on_init(environment)
#         self.start_candle = True
#         self.candle = Candlestick(0.0, False)
#
#     def on_bid_change(self, time, bid, ask):
#         # print(time,bid)
#         if self.start_candle:
#             self.candle = Candlestick(bid)
#             self.start_candle = False
#         else:
#             self.candle.add(bid, ask)
#
#     def get_candle(self):
#         self.start_candle = True
#         return self.candle


if __name__ == "__main__":
    cs1=Candlestick(1.0)
    cs1.add(1.1,1.2)
    cs1.add(1.2,1.25)
    cs1.add(0.8,1.0)

    cs2=Candlestick(1.0)
    cs2.add(1.1,1.2)
    cs2.add(1.3,1.35)
    cs2.add(0.7,0.8)

    print(cs1,cs1.spread)
    print(cs2,cs2.spread)

    cs1.add_candle(cs2)

    print(cs1,cs1.spread)
