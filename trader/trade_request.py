# -*- coding: utf-8 -*-
__author__ = 'Vit'

class TradeRequest:
    BUY="BUY"
    SELL="SELL"

    def __init__(self, type, callback=lambda time,value:None, comment=""):
        self.type=type
        self.callback=callback
        self.comment=comment

    def is_buy(self):
        return self.type==TradeRequest.BUY

    def is_sell(self):
        return self.type==TradeRequest.SELL

    def __repr__(self):
        return self.type.__str__()

if __name__ == "__main__":
    pass