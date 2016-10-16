# -*- coding: utf-8 -*-
__author__ = 'Vit'
from datetime import timedelta

from model.base_classes import AbstractSolver
from model.solvers.candlestick_solver import CandlestickSolver
# from model.solvers.moving_average import MovingAverage
from model.solvers.moving_average import MovingAverage
from model.solvers.macd import MACD
# from model.solvers.dms import DMS
from model.solvers.volume import VolumeSolver
from model.signals.trade_allower import TradeAllow
from model.signals.dms_signal import DMSSignal
from model.signals.ma_trend_signal import MATrendSignal
from trader.trade_request import TradeRequest
from model.solvers.dms import DMS
from model.signals.ma_variation import MomentumMA
from model.solvers.fractals import Fractals

class SimpleAdvisor(AbstractSolver):
    def __init__(self, period_in_sec, handler, logger, trader):
        self.period_in_sec = period_in_sec
        self.delta = timedelta(seconds=period_in_sec)
        self.logger = logger
        self.trader = trader

        # создаем необходимые солверы
        self.candle = CandlestickSolver(period_in_sec)
        self.candle5= CandlestickSolver(period_in_sec*5)
        self.ma1 = MovingAverage(period_in_sec, 60)
        self.ma5 = MovingAverage(period_in_sec*5, 60)
        self.macd1 = MACD(self.ma1, 12, 26, 9)
        # self.macd2 = MACD(self.ma2, 12, 26, 9)
        self.dms = DMS(self.candle, 60)
        # self.dms_new=DMSNew(self.candle,60)
        self.momentum=MomentumMA(self.ma1,20,20,60)
        self.fract=Fractals(self.candle,60)

        self.volume = VolumeSolver(period_in_sec, 60)
        self.trade_allow = TradeAllow()
        self.dms_signal = DMSSignal(self.dms)
        self.ma_signal = MATrendSignal(self.candle,self.ma1,30)
        self.ma_signal5 = MATrendSignal(self.candle5,self.ma5,30)


        # добавляем их в нужном порядке в обработку

        # сначала служебные и расчетные
        handler.add_solver(self.trade_allow)
        handler.add_solver(self.candle)
        handler.add_solver(self.candle5)
        handler.add_solver(self.dms)
        handler.add_solver(self.fract)

        handler.add_solver(self.ma1)
        handler.add_solver(self.macd1)
        handler.add_solver(self.ma5)
        # handler.add_solver(self.macd2)
        handler.add_solver(self.volume)
        handler.add_solver(self.ma_signal)
        handler.add_solver(self.ma_signal5)

        # потом сигналы
        handler.add_solver(self.dms_signal)
        handler.add_solver(self.momentum)


        # добавляем себя в конец обработки
        handler.add_solver(self)

        # подготовка к торговле
        self.start_time = None

        self.old_ma14 = None
        self.old_ma60 = None
        # self.old_pdi_ndi_diff=None

    def on_init(self, environment):
        super().on_init(environment)
        self.next_time = self.env.start_time + self.delta
        self.start_time = self.env.start_time

        self.log = self.logger.new_csv_file(self.env.start_time.isoformat('_').replace(':', '-'),
                                            ['SA', self.period_in_sec])
        self.log.out("Time; CSin; CSmax; CSmin; CSout; MA20; MA60; TR; ATR10; +DM; -DM; +DI10; -DI10; DXI; ADXi; Vol;"
                     "  TS; DMS_TS; MACD; MACDsig; MACDDiff; MABsig; MASsig; MABsig5; MASsig5; MAmomentum;MAmomAVG; LocMax; LocMin")
        self.log.new_line()

        self.trade_allow.trade_delay(timedelta(minutes=60))

    def on_bid_change(self, time, bid, ask):
        # print('Tick:',time.isoformat(' '),';', bid.__str__().replace('.',','))
        self.spread=ask-bid

        if time >= self.next_time:
            self._trade()

            self._log(time)
            self.next_time += self.delta


    def _trade(self):
        ma14 = self.ma1.get_lma(14)
        ma60 = self.ma1.get_lma(60)
        # pdi_ndi_diff=self.dms.get_pdi(14)-self.dms.get_ndi(14)

        self.trade_signal = 0.0

        if self.trade_allow.is_trade_allowed():
            p_ma14 = ma14 - self.old_ma14
            p_ma60 = ma60 - self.old_ma60
            if p_ma14 > 0.00001 and p_ma60 > 0.00001:
                if self.dms_signal.buy_signal > 0.5 and self.ma_signal5.average_buy_signal > 0.5:
                    self.trader.order_send(TradeRequest(TradeRequest.BUY))
                    self.trade_signal = 1.0

        self.old_ma14 = ma14
        self.old_ma60 = ma60
        # self.old_pdi_ndi_diff=pdi_ndi_diff

    def _log(self, time):

        # print(self.dms.get_adxi(14)-self.dms_new.get_adxi(14))

        self.log.out_datatime(time)
        candlestick = self.candle.get_candle()

        self.log.out(candlestick.csv_format())
        self.log.out_float(self.ma1.get_lma(20))
        self.log.out_float(self.ma1.get_lma(60))
        self.log.out_float(self.dms.get_tr())
        self.log.out_float(self.dms.get_atr_linear(14))
        self.log.out_float(self.dms.get_pdm())
        self.log.out_float(self.dms.get_ndm())
        self.log.out_float(self.dms.get_pdi(14))
        self.log.out_float(self.dms.get_ndi(14))
        self.log.out_float(self.dms.get_dxi(14))
        self.log.out_float(self.dms.get_adxi(14))
        self.log.out_float(self.volume.get_volume_average(14))
        # self.log.out_float(self.candle.get_candle().spred)
        self.log.out_float(self.trade_signal * 100)
        self.log.out_float(self.dms_signal.buy_signal * 80)
        self.log.out_float(self.macd1.macd)
        self.log.out_float(self.macd1.signal)
        self.log.out_float(self.macd1.macd-self.macd1.signal)
        self.log.out_float(self.ma_signal.average_buy_signal*100)
        self.log.out_float(self.ma_signal.average_sell_signal*100)
        self.log.out_float(self.ma_signal5.average_buy_signal*100)
        self.log.out_float(self.ma_signal5.average_sell_signal*100)
        self.log.out_float(self.momentum.get_momentum_lma(10)/self.spread/20.0)
        self.log.out_float(self.momentum.get_ema_momentum_lma(10)/self.spread/20.0)
        self.log.out_float(self.fract.max_ind())
        self.log.out_float(self.fract.min_ind())

        self.log.new_line()

    def on_de_init(self):
        self.log.close()


if __name__ == "__main__":
    pass
