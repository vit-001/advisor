# -*- coding: utf-8 -*-
__author__ = 'Vit'

class AbstractSolver:
    def on_init(self, environment):
        self.env = environment

    def on_de_init(self): pass

    def on_bid_change(self, time, bid, ask): pass

#
# class CSVwriter:
#     def csv_string(self):
#         raise RuntimeError("Метод csv_string не переопределен в классе " + self.__class__.__name__)
