# -*- coding: utf-8 -*-
__author__ = 'Vit'

from model.tick_handler import TickHandler
from model.advisors.simple_advisor2 import SimpleAdvisor
from trader.trader import Trader


def print_candle(candle, time):
    print(time, end=" ")
    candle.print()


class StrategyTester:
    """
    Класс тестирования торговой стратегии
    Предназначен для инициализации торговых стратегий с передачей им параметров и общего логгера
    Создает один или несколько TickHandler'ов и добавляет их в тикер.
    Создает торговую стратегию с определенными параметрами.
    Создает трейдер и привязывает его к торговой стратегии
    """

    def __init__(self, ticker, logger,  plotter):
        self.logger = logger
        self.plotter=plotter
        self.ticker=ticker

        self.init_strategy()

    def init_strategy(self):
        self.trader=Trader()
        self.ticker.add_tick_handler(self.trader)

        self.test_handler = TickHandler()
        self.ticker.add_tick_handler(self.test_handler)


        simple_advisor = SimpleAdvisor(60*10, self.test_handler, self.logger,self.plotter, self.trader)

if __name__ == "__main__":
    pass
