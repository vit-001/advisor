# -*- coding: utf-8 -*-
__author__ = 'Nikitin'
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick2_ohlc,candlestick_ohlc
from matplotlib.dates import date2num

class Plotter:
    def __init__(self):
        self._current_candles=dict()
        self._candles=dict()

        self._viewports=list()
        self._labels_config=dict()
        self._values=dict()
        self._times=list()

        self._dots=dict()

        self._async_graphs=dict()

        self._started=False

        self.add_viewport(list())

    def add_candle_type(self, label, width_in_sec, alfa=1.0, colorup='k',colordown='r' ):
        quotes=list()

        self._candles[label]=(quotes, width_in_sec/(24.0*3600.0), alfa, colorup, colordown)

    def add_viewport(self, label_list=list()):
        if self._started:
            raise RuntimeError('Plotter: форматирование не закончено до передачи первого фрейма')

        vp=dict()

        for label in label_list:
            vp[label]=list()
            self.config_label(label)
        self._viewports.append(vp)

    def add_label_to_viewport(self,viewport_no, label):
        self._viewports[viewport_no][label]=list()
        self.config_label(label)

    def config_label(self,label, linestyle='-', linewidth=1.0, marker=None):
        config=self._labels_config.get(label,dict())
        config['ls']=linestyle
        config['lw']=linewidth
        config['marker']=marker
        self._labels_config[label]=config


    def set_time(self,time):
        self._current_time=date2num(time)

    def draw_candle(self, label, candlestick):
        self._current_candles[label]=candlestick

    def draw_value(self,label,value):
        """
        Добавление значения в текущий фрейм
        Метки, не определенные в методе add_viewport(self, label_list) игнорируются

        :param label: метка значеня
        :param value: значение
        """
        self._values[label]=value

    def add_dots(self,label,viewport, marker='o', markersize=10.0, text_xyoffset_in_points=(-15, 10)):
        times=list()
        values=list()
        texts=list()
        marker_def=(marker,markersize)
        self._dots[label]=(times,values,texts,viewport,marker_def,text_xyoffset_in_points)

    def draw_dot(self,label,time,value,text=None):
        (times,values,texts,viewport,marker,offset)=self._dots[label]
        times.append(date2num(time))
        texts.append(text)
        values.append(value)

    def add_async_grath(self,label,viewport, linestyle='-', linewidth=1.0, marker=None):
        graph=dict()
        graph['viewport']=viewport
        graph['linestyle']=linestyle
        graph['linewidth']=linewidth
        graph['marker']=marker
        graph['times']=list()
        graph['values']=list()

        self._async_graphs[label]=graph

    def draw_async_grath(self,label,time,value):
        self._async_graphs[label]['times'].append(time)
        self._async_graphs[label]['values'].append(value)

    def next_frame(self):

        self._times.append(self._current_time)

        # добавляем свечки в массивы свечек
        for label in self._current_candles:
            candle=self._current_candles[label]
            (quotes,w,a,cu,cd) = self._candles[label]
            quotes.append((self._current_time, candle.open,candle.high,
            candle.low,candle.close))  # time, ohlc

        # добавляем значения в остальные фреймы
        for vp in self._viewports:
            for label in vp:
                vp[label].append(self._values.get(label,None))

        self._values=dict()
        self._current_candles=dict()
        self._started=True



    def plot(self):
        print('Запускаем плоттер')
        f = plt.figure()
        plt.subplots_adjust(hspace=0.001,left=0.05,right=0.99, top=0.96, bottom=0.05)

        num_subplot=len(self._viewports)

        axises=list()

        ax1 = plt.subplot(num_subplot*100+11)

        axises.append(ax1)
        # candlestick2_ohlc(ax1, self._open, self._high, self._low ,self._close, width=0.8)

        for label in self._candles:
            (quotes,w,a,cu,cd) = self._candles[label]
            candlestick_ohlc(ax1,quotes,width=w*0.8,alpha=a,colorup=cu,colordown=cd)

        # print(self.quotes)

        for i in range(num_subplot-1):
            ax = plt.subplot(num_subplot*100+i+12, sharex=ax1)
            axises.append(ax)

        for i in range(num_subplot):
            vp=self._viewports[i]
            for label in vp:
                config=self._labels_config[label]
                axises[i].plot_date(self._times, vp[label], ls=config.get('ls',), lw=config['lw'], marker=config['marker'])

        for label in self._dots:
            (times,values,texts,viewport,marker_def,offset)=self._dots[label]
            ax=axises[viewport]
            (marker,markersize)=marker_def
            ax.plot_date(times,values,marker=marker,ms=markersize)

            for i in range(len(times)):
                time=times[i]
                value=values[i]
                text=texts[i]
                if text is not None:
                    ax.annotate(text, xy=(time,value), xycoords='data',
                                xytext=offset, textcoords='offset points')


        for label in self._async_graphs:
            grath=self._async_graphs[label]
            axises[grath['viewport']].plot_date(grath['times'],grath['values'],ls=grath['linestyle'],lw=grath['linewidth'],marker=grath['marker'])

        plt.show()

if __name__ == "__main__":
    pass