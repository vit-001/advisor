# -*- coding: utf-8 -*-
__author__ = 'Vit'

import math
from base_classes import AbstractTickHandler
from datetime import timedelta


from trader.trade_request import TradeRequest

class TradePosition:
    MATRIX_SIZE = 10

    def __init__(self, open_time, bid, ask, comment, callback=lambda time,value,comment:None):
        self.comment=comment
        self.callback=callback
        self.open_bid=bid
        self.open_ask=ask+0.000032 # добавляем транзакционные издержки 0,000042
        print('Open position', self.comment)
        self.open_spread = self.open_ask - self.open_bid #todo +0.000032
        self.open_time = open_time
        self.result = [[0 for i in range(TradePosition.MATRIX_SIZE)] for j in range(TradePosition.MATRIX_SIZE)]
        self.left_zeroes = TradePosition.MATRIX_SIZE * TradePosition.MATRIX_SIZE
        self.take_profits=None
        self.stop_loses=None

    def test(self, bid, ask):
        pass

    def print_position(self):
        print()
        print('Торговая позиция', self.open_time.isoformat(' '),' спред при открытии {0:3.1f} п.'.format(self.open_spread*100000.0))
        print(self.open_bid,self.open_ask)
        if len(self.comment) >0:
            print(self.comment)
        print('   TP=         ', end='')
        for i in range(TradePosition.MATRIX_SIZE):
            print("{0:.5f}".format(self.take_profits[i]), end=' ')
        print()
        print('   SL=         ', end='')
        for i in range(TradePosition.MATRIX_SIZE):
            print("{0:.5f}".format(self.stop_loses[i]), end=' ')
        print()

        print('   Profit/loss=', end='')
        for i in range(TradePosition.MATRIX_SIZE):
            print("  {0:.1f}  ".format(self.open_spread*(i+1)/0.0001), end=' ')
        print(' пунктов')

        for i in range(TradePosition.MATRIX_SIZE):
            for j in range(TradePosition.MATRIX_SIZE):
                print("{0: 6.0f}".format(self.result[i][j]/60), end='')
            print()

        print('   Пустые элеиенты таблицы', self.left_zeroes)
        print()


class BuyPosition(TradePosition):
    def __init__(self, open_time, bid, ask, comment, callback):
        super().__init__(open_time, bid, ask, comment, callback)
        self.take_profits = [ask + self.open_spread * (i + 1) for i in range(TradePosition.MATRIX_SIZE)]
        self.stop_loses = [bid - self.open_spread * (i + 1) for i in range(TradePosition.MATRIX_SIZE)]

    def test(self, time, bid, ask=0.0):
        if self.left_zeroes==0:
            return
        seconds = (time - self.open_time).total_seconds()
        if seconds < 1.0: seconds = 1.0
        for i in range(TradePosition.MATRIX_SIZE):
            if bid >= self.take_profits[i]:
                for j in range(TradePosition.MATRIX_SIZE):
                    if self.result[i][j] == 0:
                        self.result[i][j] = seconds
                        self.left_zeroes -= 1
        for j in range(TradePosition.MATRIX_SIZE):
            if bid <= self.stop_loses[j]:
                for i in range(TradePosition.MATRIX_SIZE):
                    if self.result[i][j] == 0:
                        self.result[i][j] = -seconds
                        self.left_zeroes -= 1

    def plot_position(self,take_profit_in_spreads,stop_loss_in_spreads):
        result=self.result[take_profit_in_spreads][stop_loss_in_spreads]/60
        self.callback(self.open_time,self.open_ask,'Buy {0: 4.0f}'.format(result))
        print("Open on:",self.open_time,"close on:",self.open_time+timedelta(seconds=abs(int(result*60))),int(result))

class SellPosition(TradePosition):
    def __init__(self, time, bid, ask, comment, callback):
        super().__init__(time, bid, ask, comment, callback)
        self.take_profits = [bid - self.open_spread * (i + 1) for i in range(TradePosition.MATRIX_SIZE)]
        self.stop_loses = [bid + self.open_spread * (i + 1) for i in range(TradePosition.MATRIX_SIZE)]

    def test(self, time, bid, ask=0.0):
        if self.left_zeroes==0:
            return
        seconds = (time - self.open_time).total_seconds()
        if seconds < 1.0: seconds = 1.0
        for i in range(TradePosition.MATRIX_SIZE):
            if ask <= self.take_profits[i]:
                for j in range(TradePosition.MATRIX_SIZE):
                    if self.result[i][j] == 0:
                        self.result[i][j] = seconds
                        self.left_zeroes -= 1
        for j in range(TradePosition.MATRIX_SIZE):
            if ask >= self.stop_loses[j]:
                for i in range(TradePosition.MATRIX_SIZE):
                    if self.result[i][j] == 0:
                        self.result[i][j] = -seconds
                        self.left_zeroes -= 1

    def plot_position(self,take_profit_in_spreads,stop_loss_in_spreads):
        result=self.result[take_profit_in_spreads][stop_loss_in_spreads]/60
        self.callback(self.open_time,self.open_bid,'Sell {0: 4.0f}'.format(result))

class Trader(AbstractTickHandler):
    def __init__(self):
        # self.request = None
        self.open_positions = list()
        self.requests=list()
        # self.echo=echo_file

    def order_send(self, request):
        # print(request)
        self.requests.append(request)

    def on_tick(self, tick):

        if len(self.requests)>0:
            for request in self.requests:
                print(request, 'on tick:')
                print(tick)
                if request.is_buy():
                    self.open_positions.append(BuyPosition(tick.time,tick.bid,tick.ask, request.comment,request.callback))
                    # request.callback(tick.time,tick.ask)
                if request.is_sell():
                    self.open_positions.append(SellPosition(tick.time,tick.bid,tick.ask, request.comment,request.callback))
                    # request.callback(tick.time,tick.bid)
            self.requests = list()


        for position in self.open_positions:
            position.test(tick.time,tick.bid,tick.ask)

    def on_de_init(self):
        for position in self.open_positions:
            position.print_position()

        self.print_statistic()

    def plot_positions(self,take_profit_in_spreads,stop_loss_in_spreads):
        print('Результат открытых позиций')
        print('============')
        for pos in self.open_positions:
            pos.plot_position(take_profit_in_spreads,stop_loss_in_spreads)
        print('============')

    def print_statistic(self):
        print('Статистика по всем открытым позициям:')
        positions=len(self.open_positions)
        print('   Количество позиций', positions, end=', ')

        opened=0
        for pos in self.open_positions:
            if pos.left_zeroes>0:
                opened +=1
        print('из них полностью не закрытых', opened)

        if positions==0:
            return

        print('   Матрица результата:')
        max_profit=-TradePosition.MATRIX_SIZE*100.0
        for i in range(TradePosition.MATRIX_SIZE):
            for j in range(TradePosition.MATRIX_SIZE):
                win=0.0
                profit=0.0
                for pos in self.open_positions:
                    # win += math.copysign(1.0, pos.result[i][j])
                    if pos.result[i][j]>0.0:
                        profit += 1.0    #float(i+1)/float(j+1)
                        win+=1.0
                    else:
                        profit -= float(j+2)/float(i+1)
                if profit>max_profit:
                    max_profit=profit
                print("{0: 4.0f}%({1: 4.2f})".format(win/positions*100.0,profit), end='')
            print()
        print('Максимальный выигрыш:{0: 4.2f} * ставки'.format(max_profit))
        print()

    def print2(self,*data,**kw):
        for t in data:

            print(t,end=' ')
        print()



if __name__ == "__main__":
    from datetime import datetime, timedelta

    start = datetime(1970, 1, 1, 1, 1, 1)
    td = timedelta(seconds=1)

    tp = BuyPosition(start, 1.1, 1.2)
    print(tp.result)
    print(tp.take_profits)
    print(tp.stop_loses)

    tp.test(start, 1.1)
    tp.test(start + td, 1.31)
    tp.test(start + td + td, 1.4)
    tp.test(start + td + td + td, 0.95)
    tp.test(start + td + td + td + td, 0.85)

    tp.test(start + td + td + td, 0.95)
    tp.test(start + td + td + td + td, 0.85)