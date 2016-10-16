# -*- coding: utf-8 -*-
__author__ = 'Vit'


class AbstractTickHandler:
    def on_init(self, environment): pass

    def on_de_init(self): pass

    def on_tick(self, tick): pass
