# -*- coding: utf-8 -*-
__author__ = 'Nikitin'
from datetime import datetime

from ticker.tick import Tick


class MultiFileTicker:
    """
    Класс отвечает за выдачу списку получателей последовательности тиков из файла выгруженных данных.
    Формат файла в соответствии с номерами версии INPUT_FILE_VERSION, которые
    должны быть указаны в первой строке файла.
    Использование:
        Создать экземпляр класса
        Зарегистрировать всех получателей последовательностей тиков при помощи add_tick_handler
            В получателе должны быть определены методы:
                on_init(self, environment)
                on_de_init(self)
                on_tick(self, tick)
        Запустить процесс методом start

    """
    INPUT_FILE_VERSION = ["2.1", "2.0"]

    def __init__(self):
        self.tick_handlers = list()
        self.tick_count = 0
        self.first_file = True

    def add_tick_handler(self, handler):
        self.tick_handlers.append(handler)

    def start(self, input_filenames_iterator, environment):

        for fname in input_filenames_iterator:
            file = open(fname)
            self._proceed_file_header(file, environment)
            print(fname, "запущен")
            for line in file:
                new_tick = Tick(line)
                # print(new_tick)
                self.last_tick_time = new_tick.time
                self.tick_count += 1
                for handler in self.tick_handlers:
                    handler.on_tick(new_tick)

        for handler in self.tick_handlers:
            handler.on_de_init()

    def duration(self):
        return self.last_tick_time - self.start_time

    def _proceed_file_header(self, file, environment):
        version = file.readline().strip()
        if version not in MultiFileTicker.INPUT_FILE_VERSION:
            raise RuntimeError(
                "Неверная версия файла uld - должна быть " + MultiFileTicker.INPUT_FILE_VERSION.__str__())
        if self.first_file:
            environment.symbol = file.readline().strip()
            info = file.readline().strip().split(";")
            environment.start_time = datetime.strptime(info[0], "%Y.%m.%d %H:%M")
            self.start_time = environment.start_time
            environment.digits = int(info[1])
            environment.point = float(info[2])

            self._start_tick_handlers(environment)  # запускаем advisor'ы только после чтения заголовка 1-го файла

            self.first_file = False
        else:
            if file.readline().strip() != environment.symbol:
                raise RuntimeError("Символ файла не соответствует символу первого файла")
            file.readline()
        file.readline()
        file.readline()
        file.readline()

    def _start_tick_handlers(self, environment):
        for handler in self.tick_handlers:
            print("Обработчик", handler.__class__.__name__, "запущен")
            handler.on_init(environment)

if __name__ == "__main__":
    pass
