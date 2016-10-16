# -*- coding: utf-8 -*-
__author__ = 'Vit'

from datetime import datetime


class Environment:
    def __init__(self):
        self.symbol = ""
        self.start_time = datetime(1970, 1, 1)
        self.digits = 5
        self.point = 0.00001000


if __name__ == "__main__":
    pass
