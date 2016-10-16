# -*- coding: utf-8 -*-
__author__ = 'Vit'
from environment.constant import Constant
from base_classes import AbstractTickHandler


class TickHandler(AbstractTickHandler):
    """
    Класс определяет стандартный обработчик тиков
    Его функция - получить последовательность тиков, отфильтровать из них тики с изменением значения BID
    и передать их по очереди всем зарегистрированным solver'ам (интерфейс model.base_classes.AbstractSolver)
    Использование:
        создать экземпляр класса
        зарегистрировать его в тикере
        добавить solver'ы методом add_solver
    """
    def __init__(self):
        self.solvers = list()

    def add_solver(self, solver):
        self.solvers.append(solver)

    def on_init(self, environment):
        self.env = environment
        for solver in self.solvers:
            solver.on_init(environment)
            print("  модуль", solver.__class__.__name__, "запущен")
        print("Символ", self.env.symbol)
        print("Старт прогона", self.env.start_time)

        self.bid_change_count = 0
        self.tick_count = 0

    def on_de_init(self):
        for solver in self.solvers:
            solver.on_de_init()
        print('Тиков получено', self.tick_count)
        print('Значение BID поменялось', self.bid_change_count, 'раз')
        pass

    def on_tick(self, tick):
        self.tick_count += 1
        if tick.flags & Constant.TICK_FLAG_BID:
            self.bid_change_count += 1
            # print(tick)
            for solver in self.solvers:
                solver.on_bid_change(tick.time, tick.bid, tick.ask)


if __name__ == "__main__":
    pass
