# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

from datetime import timedelta
from model.base_classes import AbstractSolver

class TradeAllow(AbstractSolver):
    def __init__(self):
        self.trade_allow=False
        self.trade_allow_time=None

    def on_init(self, environment):
        super().on_init(environment)
        self.current_time=self.env.start_time

    def on_bid_change(self, time, bid, ask):
        self.current_time=time
        self._trade_session()
        if self.trade_allow_time is None:
            return
        if time > self.trade_allow_time:
            self.trade_allow=True
            self.trade_allow_time=None

    def trade_delay(self, time_delta):
        self.trade_allow=False
        if self.trade_allow_time is not None:
            if self.current_time+time_delta < self.trade_allow_time:
                return
        self.trade_allow_time=self.current_time+time_delta

    def is_trade_allowed(self):
        return self.trade_allow

    def _trade_session(self):
        if self.current_time.hour>22:
            self.trade_delay(timedelta(minutes=180))
        pass

if __name__ == "__main__":
    pass