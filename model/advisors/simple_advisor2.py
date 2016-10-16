# -*- coding: utf-8 -*-
__author__ = 'Vit'
from datetime import timedelta

from model.base_classes import AbstractSolver

from model.solvers.candlestick_solver import CandlestickSolver
from model.solvers.moving_average import MovingAverage
from model.solvers.macd import MACD
from model.solvers.moving_average_array import MovindAverageSimpleArray
from model.solvers.dms import DMS
# from model.solvers.fractals2 import Fractals
from model.solvers.moving_average_cs import MovingAverage as MA_cs

from model.signals.trade_allower import TradeAllow
from model.signals.ma_trend_signal import MATrendSignal
from model.signals.ma_variation import MomentumMA
from model.signals.dms_signal import DMSSignal

# from model.signals.fractals_trade_signal import FractalsTradeSignal

from model.patterns.rebound_pattern import ReboundPatternSignal
from model.patterns.rebound_pattern2 import ReboundPatternSignal as ReboundPatternSignal2

from trader.trade_request import TradeRequest

class SimpleAdvisor(AbstractSolver):
    def __init__(self, period_in_sec, handler, logger, plotter, trader):
        self.period_in_sec = period_in_sec
        self.delta = timedelta(seconds=period_in_sec)
        self.logger = logger
        self.trader = trader
        self.plotter=plotter


        # ПАРАМЕТРЫ
        self.period_multiplier = 5  # соотношение между двумя периодами анализа
        self.ma_period = 20
        self.momentum_period1 = 4
        self.momentum_period2 = 10

        # создаем необходимые солверы
        self.candle0 = CandlestickSolver(60)
        self.candle1 = CandlestickSolver(period_in_sec)
        self.candle2 = CandlestickSolver(period_in_sec * self.period_multiplier)

        self.ma1 = MovingAverage(period_in_sec, 60)
        self.ma2 = MovingAverage(period_in_sec * self.period_multiplier, 60)
        self.ma_cs=MA_cs(self.candle0,200)

        self.macd = MACD(self.ma1, 12, 26, 9)
        # self.macd2 = MACD(self.ma2, 12, 26, 9)
        self.dms = DMS(self.candle1, 60)
        # self.dms_new=DMSNew(self.candle,60)
        self.momentum1 = MomentumMA(self.ma1, self.ma_period, 60)
        self.momentum2 = MomentumMA(self.ma2, self.ma_period, 60)

        # self.fract=Fractals(self.candle1,lambda time,value: None,self.on_min_fractal)

        # self.volume = VolumeSolver(period_in_sec, 60)
        self.trade_allow = TradeAllow()

        self.dms_signal = DMSSignal(self.dms)

        self.ma_signal1 = MATrendSignal(self.candle1, self.ma1, self.ma_period)
        self.ma_signal2 = MATrendSignal(self.candle2, self.ma2, self.ma_period)

        # self.fract_signal=FractalsTradeSignal(self.ma1,self.candle1)
        self.rebound_signal=ReboundPatternSignal(self.ma1,self.candle1)
        self.rebound_signal.set_on_pattern_found_handlers(on_high_found=lambda time,value: self.plotter.draw_dot('max',time,value),
                                                          on_low_found=lambda time,value:self.plotter.draw_dot('min',time,value))

        # self.rebound_signal2=ReboundPatternSignal2(self.candle0)
        # self.rebound_signal.set_on_pattern_found_handlers(on_high_found=lambda time,value: self.plotter.draw_dot('max2',time,value),
        #                                                   on_low_found=lambda time,value:self.plotter.draw_dot('min2',time,value))


        # self.candle0.add_handler(self.trade_on_m1_candle)
        # добавляем их в нужном порядке в обработку

        # сначала служебные и расчетные
        handler.add_solver(self.trade_allow)
        handler.add_solver(self.candle0)
        handler.add_solver(self.candle1)
        handler.add_solver(self.candle2)
        handler.add_solver(self.dms)
        # handler.add_solver(self.fract)

        handler.add_solver(self.ma1)
        handler.add_solver(self.ma2)
        handler.add_solver(self.macd)

        # handler.add_solver(self.macd2)
        # handler.add_solver(self.volume)
        handler.add_solver(self.ma_signal1)
        handler.add_solver(self.ma_signal2)

        # потом сигналы
        handler.add_solver(self.dms_signal)
        handler.add_solver(self.momentum1)
        handler.add_solver(self.momentum2)
        # handler.add_solver(self.fract_signal)
        handler.add_solver(self.rebound_signal)


        # добавляем себя в конец обработки
        handler.add_solver(self)

        # подготовка к торговле
        self.start_time = None

        # self.old_abs1 = 0.0  # предыдущее значение MATrendSignal(self.candle1,self.ma1,30).average_buy_signal
        # self.old_momentum1_1 = 1.0

        self.trade_interval=20
        self.trade_wait=0

        # self.old_ma60 = None
        # self.old_pdi_ndi_diff=None

        # вспомогательные переменные

        self.spread_arr = MovindAverageSimpleArray(60)

    def on_init(self, environment):
        super().on_init(environment)
        self.next_time = self.env.start_time + self.delta
        self.start_time = self.env.start_time

        self.trade_allow.trade_delay(timedelta(minutes=60))

        self._log_config()
        self._plot_config()



    def on_bid_change(self, time, bid, ask):
        # print('Tick:',time.isoformat(' '),';', bid.__str__().replace('.',','))
        self.spread = ask - bid
        self.spread_arr.on_change(self.spread)



        if time >= self.next_time:

            self.fractal_signal_value=self.rebound_signal.buy_signal    #self.fract_signal.signal
            self.fractal_delta_value=self.rebound_signal.buy_delta      #self.fract_signal.delta

            # self.fractal_signal_value2=self.rebound_signal2.buy_signal

            self._trade()

            self._log(time)
            self._plot(time)
            self.next_time += self.delta


    def trade_on_m1_candle(self,time,candle):
        self.fractal_signal_value2=self.rebound_signal2.buy_signal
        if self.trade_allow.is_trade_allowed(): # and self.trade_wait > self.trade_interval:

            if self.fractal_signal_value2 > 5.0:

                    self.trader.order_send(TradeRequest(TradeRequest.BUY,lambda time,value,comment: self.plotter.draw_dot('trade',time,value,comment),
                                                        'Fractal signal={0: 4.2f}'.format(self.fractal_signal_value2)))


    def _trade(self):
        #
        #
        # ma14 = self.ma1.get_lma(14)
        # ma60 = self.ma1.get_lma(60)
        # pdi_ndi_diff=self.dms.get_pdi(14)-self.dms.get_ndi(14)

        self.trade_wait +=1

        self.trade_signal = 0.0
        # abs1=self.ma_signal1.average_buy_signal
        momentum1_1 = self.momentum1.get_momentum_lma(self.momentum_period1) / self.spread_arr.get_ema(
            60) / self.momentum_period1

        if self.trade_allow.is_trade_allowed(): # and self.trade_wait > self.trade_interval:
            if self.fractal_signal_value>5.0:
            # if (self.ma_signal2.average_buy_signal > 0.5 and
            #                 self.momentum2.get_momentum_lma(
            #                     self.momentum_period2) / self.momentum_period2 > self.spread_arr.get_ema(60) * 0.5):
            #
            #     if self.dms_signal.buy_signal > 0.5:
                    # торгуем здесь

                    self.trade_signal = 1.0
                    self.trader.order_send(TradeRequest(TradeRequest.BUY,lambda time,value,comment: self.plotter.draw_dot('trade',time,value,comment),
                                                        'Fractal signal={0: 4.2f}'.format(self.fractal_signal_value)))
                    self.trade_wait=0


        # self.old_abs1=abs1
        # self.old_momentum1_1 = momentum1_1


    # def on_min_fractal(self,time,value):
        # self.plotter.draw_dot('min',time,value)
        # self.fract_signal.on_min_fractal(time,value)


    def _plot_config(self):
        self.plotter.add_viewport(('frSig','frSig2'))
        self.plotter.add_viewport(('+DI','-DI','ADXI'))
        self.plotter.add_viewport(('MACD','MACDsig'))
        self.plotter.add_label_to_viewport(0,'MA')
        self.plotter.add_label_to_viewport(0,'MA_cs')
        self.plotter.config_label('ADXI',linewidth=2.0)
        self.plotter.add_candle_type('CS1',self.period_in_sec, alfa=0.5)
        self.plotter.add_candle_type('CS2',self.period_in_sec*self.period_multiplier,alfa=0.5,colorup='grey',colordown='yellow')
        self.plotter.add_dots('trade',0,'>',text_xyoffset_in_points=(-15, 30))
        self.plotter.add_dots('max',0,'^')
        self.plotter.add_dots('min',0,'v')
        # self.plotter.add_dots('max2',0,'^')
        # self.plotter.add_dots('min2',0,'v')


        self._f_sig_ploted=False

    def _plot(self, time):
        self.plotter.set_time(time)
        self.plotter.draw_candle('CS1',self.candle1.get_candle())
        # if abs(time-self.candle2.candle_time)<timedelta(seconds=self.period_in_sec-1):
        #     self.plotter.draw_candle('CS2',self.candle2.get_candle())
        self.plotter.draw_value('+DI',self.dms.get_pdi(14))
        self.plotter.draw_value('-DI',self.dms.get_ndi(14))
        self.plotter.draw_value('ADXI',self.dms.get_adxi(14))

        # self.plotter.draw_value('MABSig1',self.ma_signal1.average_buy_signal)
        # self.plotter.draw_value('MABSig2',self.ma_signal2.average_buy_signal)

        self.plotter.draw_value('MA',self.ma1.get_lma(14))
        if (time-self.env.start_time)> timedelta(minutes=140):
            self.plotter.draw_value('MA_cs',self.ma_cs.typical.get_lma(14*10))

        self.plotter.draw_value('MACD',self.macd.macd)
        self.plotter.draw_value('MACDsig',self.macd.signal)

        self.plotter.draw_value('frSig',self.fractal_signal_value)
        # self.plotter.draw_value('frSig2',self.fractal_signal_value2)
        # print(self.fractal_signal_value,self.fractal_signal_value2)

        # self.plotter.draw_value('frDelta',self.fractal_delta_value)

        self.plotter.next_frame()

    def _log_config(self):
        self.log = self.logger.new_csv_file(self.env.start_time.isoformat('_').replace(':', '-'),
                                            ['SA2', self.period_in_sec])
        self.log.out("Time; CSin; CSmax; CSmin; CSout; MA1-20; MA2-20; MAmomentum1-1;MAmomentum1-2; MAmomentum2-2; "
                     "MABSig1; MABSig2; Trade; DMSSignal; +DI; -DI; ADXI; ")
        self.log.new_line()

    def _log(self, time):
        # print(self.dms.get_adxi(14)-self.dms_new.get_adxi(14))

        self.log.out_datatime(time)
        candlestick = self.candle1.get_candle()
        self.log.out(candlestick.csv_format())
        # self.plotter.draw_dot('CSin',time,candlestick.open)


        self.log.out_float(self.ma1.get_lma(self.ma_period))
        self.log.out_float(self.ma2.get_lma(self.ma_period))

        ma_spread = self.spread_arr.get_ema(60)

        self.log.out_float(self.momentum1.get_momentum_lma(self.momentum_period1) / ma_spread / self.momentum_period1)
        self.log.out_float(self.momentum1.get_momentum_lma(self.momentum_period2) / ma_spread / self.momentum_period2)
        self.log.out_float(self.momentum2.get_momentum_lma(self.momentum_period2) / ma_spread / self.momentum_period2)

        self.log.out_float(self.ma_signal1.average_buy_signal * 100)
        self.log.out_float(self.ma_signal2.average_buy_signal * 100)

        # self.log.out_float(self.trade_signal * 110.0)
        self.log.out_float(self.dms_signal.buy_signal*60.0)



        # self.log.out_float(self.dms.get_tr())
        # self.log.out_float(self.dms.get_atr_linear(14))
        # self.log.out_float(self.dms.get_pdm())
        # self.log.out_float(self.dms.get_ndm())
        self.log.out_float(self.dms.get_pdi(14))
        self.log.out_float(self.dms.get_ndi(14))
        # self.log.out_float(self.dms.get_dxi(14))
        self.log.out_float(self.dms.get_adxi(14))
        # self.log.out_float(self.volume.get_volume_average(14))
        # # self.log.out_float(self.candle.get_candle().spred)

        # self.log.out_float(self.dms_signal.buy_signal * 80)
        # self.log.out_float(self.macd1.macd)
        # self.log.out_float(self.macd1.signal)
        # self.log.out_float(self.macd1.macd-self.macd1.signal)
        # self.log.out_float(self.ma_signal.average_buy_signal*100)
        # self.log.out_float(self.ma_signal.average_sell_signal*100)
        # self.log.out_float(self.ma_signal5.average_buy_signal*100)
        # self.log.out_float(self.ma_signal5.average_sell_signal*100)
        #
        # self.log.out_float(self.momentum.get_ema_momentum_lma(10)/self.spread/20.0)
        # self.log.out_float(self.fract.max_ind())
        # self.log.out_float(self.fract.min_ind())



        self.log.new_line()


    def on_de_init(self):
        self.trader.plot_positions(19,9)
        self.log.close()


if __name__ == "__main__":
    pass
