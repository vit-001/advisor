# -*- coding: utf-8 -*-
__author__ = 'Vit'
from datetime import timedelta

from model.base_classes import AbstractSolver

from model.solvers.candlestick_solver import CandlestickSolver
from model.solvers.moving_average import MovingAverage
from model.solvers.macd import MACD
from model.solvers.moving_average_array import MovindAverageSimpleArray
from model.solvers.dms import DMS

from model.signals.trade_allower import TradeAllow
from model.patterns.rebound_pattern import ReboundPatternSignal
from model.patterns.rebound_pattern2 import ReboundPatternSignal as ReboundPatternSignal2

from trader.trade_request import TradeRequest

class SimpleAdvisor(AbstractSolver): # todo
    def __init__(self, period_in_sec, handler, logger, plotter, trader):
        self.period_in_sec = period_in_sec
        self.delta = timedelta(seconds=period_in_sec)
        # self.logger = logger
        self.trader = trader
        self.plotter=plotter


        # ПАРАМЕТРЫ
        # self.candle_period = 10
        # self.ma_period = 14
        # self.start_minute=3


        # создаем необходимые солверы
        self.candle_m1 = CandlestickSolver(60)
        self.candle1 = CandlestickSolver(period_in_sec)
        self.ma1 = MovingAverage(period_in_sec, 60)

        self.trade_allow = TradeAllow()

        self.rebound_signal=ReboundPatternSignal(self.ma1,self.candle1)
        self.rebound_signal.set_on_pattern_found_handlers(on_high_found=lambda time,value: self.plotter.draw_dot('max',time,value),
                                                          on_low_found=lambda time,value:self.plotter.draw_dot('min',time,value))

        self.rebound_signal2=ReboundPatternSignal2(self.candle_m1)
        self.rebound_signal2.setting(base_period=10, start_minute=3, ma_period=14)
        self.rebound_signal2.set_on_signal_handler(self.on_signal_trade)
        self.rebound_signal2.set_on_pattern_found_handlers(on_high_found=lambda time,value: self.plotter.draw_dot('max2',time,value),
                                                          on_low_found=lambda time,value:self.plotter.draw_dot('min2',time,value))
        self.rebound_signal2.set_on_candle_handler(self.on_candle)
        self.rebound_signal2.set_plot_signal_proc(self.draw_signal)


        # добавляем их в нужном порядке в обработку

        # сначала служебные и расчетные
        handler.add_solver(self.trade_allow)
        handler.add_solver(self.candle_m1)
        handler.add_solver(self.candle1)
        handler.add_solver(self.ma1)

        # потом сигналы
        handler.add_solver(self.rebound_signal)
        handler.add_solver(self.rebound_signal2)

        # добавляем себя в конец обработки
        handler.add_solver(self)

        # подготовка к торговле
        self.start_time = None

    def on_init(self, environment):
        super().on_init(environment)
        self.next_time = self.env.start_time + self.delta
        self.start_time = self.env.start_time

        self.trade_allow.trade_delay(timedelta(minutes=60))

        self._plot_config()

        self.fractal_signal_value2=0.0



    def on_bid_change(self, time, bid, ask):

        if time >= self.next_time:

            self.fractal_signal_value=self.rebound_signal.buy_signal
            # self.fractal_delta_value=self.rebound_signal.buy_delta
            # self.fractal_signal_value2=self.rebound_signal2.buy_signal

            # self.plotter.draw_async_grath('frSig2async',time,self.fractal_signal_value)

            # print('   ',self.candle1.get_candle())

            # self._trade()
            self._plot(time)

            self.next_time += self.delta

    def _trade(self):

        if self.trade_allow.is_trade_allowed():
            if self.fractal_signal_value>5.0:
                    # торгуем здесь
                    self.trader.order_send(TradeRequest(TradeRequest.BUY,lambda time,value,comment: self.plotter.draw_dot('trade',time,value,comment),
                                                        'Fractal signal={0: 4.2f}'.format(self.fractal_signal_value)))


    def on_signal_trade(self):
        self.fractal_signal_value2=self.rebound_signal2.buy_signal
        if self.trade_allow.is_trade_allowed():
            if self.fractal_signal_value2 > 5.0:
                    # торгуем здесь
                    self.trader.order_send(TradeRequest(TradeRequest.BUY,lambda time,value,comment: self.plotter.draw_dot('trade',time,value,comment),
                                                        'Fractal signal={0: 4.2f}'.format(self.fractal_signal_value2)))

    def draw_signal(self,time,value):
        self.plotter.draw_async_grath('frSig2async',time,value)

    def on_candle(self,time,candle):
        self.plotter.draw_dot('candles',time,candle.close)
        # self.plotter.draw_candle('cs2',candle)



    def _plot_config(self):
        self.plotter.add_candle_type('cs2',60*10)
        self.plotter.add_viewport(('frSig','frSig2'))
        self.plotter.add_label_to_viewport(0,'MA')
        self.plotter.add_candle_type('CS1',self.period_in_sec, alfa=0.5)

        self.plotter.add_dots('trade',0,'>',text_xyoffset_in_points=(-15, 30))
        self.plotter.add_dots('max',0,'^')
        self.plotter.add_dots('min',0,'v')
        self.plotter.add_dots('max2',0,'^')
        self.plotter.add_dots('min2',0,'v')

        self.plotter.add_dots('candles',0,'*')

        self.plotter.add_async_grath('frSig2async',1)

    def _plot(self, time):
        self.plotter.set_time(time)
        self.plotter.draw_candle('CS1',self.candle1.get_candle())

        self.plotter.draw_value('MA',self.ma1.get_lma(20))

        self.plotter.draw_value('frSig',self.fractal_signal_value)
        # self.plotter.draw_value('frDelta',self.fractal_delta_value)
        # self.plotter.draw_value('frSig2',self.fractal_signal_value2)


        self.plotter.next_frame()

    def on_de_init(self):
        self.trader.plot_positions(15,7)

if __name__ == "__main__":
    pass
