# -*- coding: utf-8 -*-
__author__ = 'Vit'

from datetime import timedelta


class AverageQuantum:
    def __init__(self):
        self.sum = 0.0
        self.n = 0

    @property
    def value(self):
        if self.n == 0:
            return 0.0
            raise RuntimeError("Недействительное значение среднего в AverageQuantum")
        return self.sum / self.n

    def add(self, value, n=1):
        self.sum += value
        self.n += n

    def add_quantum(self, average_quantum, weight=1):
        self.sum += average_quantum.sum * weight
        self.n += average_quantum.n * weight

    def __repr__(self):
        return 'AQ({0:.5},{1})'.format(self.sum, self.n)


# Массив для подсчета MA потока значений с произвольным распределением по времени
class MovindAverageArray:
    def __init__(self, quantum_in_sec, dimension):
        self.array = [AverageQuantum() for i in range(dimension)]
        self.delta = timedelta(seconds=quantum_in_sec)
        self.accumulator = AverageQuantum()

    def on_init(self, start_time):
        self.next_time = start_time + self.delta

    def on_change(self, time, value):
        if time >= self.next_time:
            # print(self.array)
            self.array.insert(0, self.accumulator)
            self.accumulator = AverageQuantum()
            self.array.pop()
            self.next_time += self.delta
        self.accumulator.add(value)

    def get_ma(self, duration_in_quantum):
        temp = AverageQuantum()
        for i in range(duration_in_quantum):
            temp.add_quantum(self.array[i])
        return temp.value

    def get_lma(self, duration_in_quantum):
        temp = AverageQuantum()
        for i in range(duration_in_quantum):
            temp.add_quantum(self.array[i], duration_in_quantum - i)
        return temp.value

    def get_ema(self,duration_in_quantum):  #todo
        raise RuntimeError('Функция MovindAverageArray.get_ema не реализована')


#
#
# # Массив для подсчета MA без учета времени, за N предыдущих отсчетов
# class MovindAverageSimpleArrayOld:
#     def __init__(self, dimension):
#         self.array = [AverageQuantum() for i in range(dimension)]
#         self.ema_dict=dict()
#
#     def on_change(self, value):
#         # print(value,n)
#         self.array.insert(0, AverageQuantum())
#         self.array.pop()
#         self.array[0].add(value)
#         for duration in self.ema_dict:
#             alfa=2.0/(duration+1)
#             self.ema_dict[duration]=alfa*value+(1-alfa)*self.ema_dict[duration]
#
#
#     def get_ma(self, duration):
#         temp = AverageQuantum()
#         for i in range(duration):
#             temp.add_quantum(self.array[i])
#         return temp.value
#
#     def get_lma(self, duration):
#         temp = AverageQuantum()
#         for i in range(duration):
#             temp.add_quantum(self.array[i], duration - i)
#         return temp.value
#
#     def _ema(self, alfa,i,n):
#         if n == 1:
#             return self.array[i].sum
#         return alfa*self.array[i].sum + (1.0 - alfa) * self._ema(alfa,i+1,n-1)
#
#     def get_ema(self,duration): # todo
#         if duration not in self.ema_dict:
#             alfa=2.0/(duration+1)
#             ema=self._ema(alfa,0,duration)
#             self.ema_dict[duration]=ema
#         return self.ema_dict[duration]


# Массив для подсчета MA без учета времени, за N предыдущих отсчетов
class MovindAverageSimpleArray:
    def __init__(self, dimension):
        self.array = [0.0 for i in range(dimension)]
        self.ema_dict=dict()
        self.n=0

    def on_change(self, value):
        self.array.insert(0, value)
        self.array.pop()
        for duration in self.ema_dict:
            alfa=2.0/(duration+1)
            self.ema_dict[duration]=alfa*value+(1-alfa)*self.ema_dict[duration]

        self.n+=1

    def get_ma(self, duration):
        temp = 0.0
        for i in range(duration):
            temp+=self.array[i]
        return temp/duration

    def get_lma(self, duration):
        if self.n==0:
            return 0.0
        if duration>self.n:
            return self.get_lma(self.n)
        temp = 0.0
        for i in range(duration):
            temp += self.array[i] *( duration - i)
        return 2.0 * temp / (duration*(duration+1))

    def _ema(self, alfa,i,n):
        if n == 1:
            return self.array[i]
        last_ema=self._ema(alfa,i+1,n-1)
        return alfa*self.array[i] + (1.0 - alfa) * last_ema

    def get_ema(self,duration): # todo
        if duration not in self.ema_dict:
            alfa=2.0/(duration+1)
            ema=self._ema(alfa,0,duration)
            self.ema_dict[duration]=ema
        return self.ema_dict[duration]

    def get_past_value(self, time_shift):
        return self.array[time_shift]

if __name__ == "__main__":
    # ma = MovindAverageSimpleArrayOld(10)
    ma2= MovindAverageSimpleArray(10)

    for i in range(10):
        # ma.on_change(i)
        ma2.on_change(i)


        # print(ma.array)
        # print(ma2.array)
        # print(ma.get_ma(5),ma2.get_ma(5))
        # print(ma.get_lma(5),ma2.get_lma(5))
        # print(ma.get_ema(5),ma2.get_ema(5))
        # print(ma.get_ema(7),ma2.get_ema(7))
