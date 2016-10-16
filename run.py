# -*- coding: utf-8 -*-
__author__ = 'Vit'

from datetime import datetime

from ticker.ticker import MultiFileTicker
from ticker.file_work.file_series import FileSeries
from environment.environment import Environment
from model.strategy_tester_test1 import StrategyTester  # todo менять типы стратегий здесь!!!
# from model.strategy_tester_work1 import StrategyTester
from model.logger.logger import Logger
from model.logger.plotter import Plotter

class Run:
    @staticmethod
    def start(path, fname_prefix, fname_suffix='.uld', fname_out_suffix='.csv'):
        # path='files/v2.1/'
        # fname_prefix='EURUSD_'
        # fname_suffix='.uld'
        # fname_out_suffix='.csv'

        print('Начинаем прогон')
        starttime = datetime.now()

        env = Environment()
        try:
            files = FileSeries(path, fname_prefix, fname_suffix)
            newticker = MultiFileTicker()
            logger = Logger(path + 'out/', fname_prefix, fname_out_suffix)
            plotter=Plotter()
            tester = StrategyTester(newticker,logger,plotter)
            newticker.start(files.iterator(), env)
        except (OSError, RuntimeError) as err:
            print(err)
            raise err
        else:
            endtime = datetime.now()
            duration_sim = newticker.duration().total_seconds()
            duration = (endtime - starttime).total_seconds()
            print("Прогон закончен за {0:.3} сек".format(duration))
            print(
                "Симулировано {0:.2f} часов, {1:.3} мин/сек".format(duration_sim / 3600, duration_sim / duration / 60))
            plotter.plot()

if __name__ == "__main__":
    import sys
    from trader.trader import TradePosition

    path = 'files/v2.1/'
    fname_prefix = 'EURUSD_'
    fname_suffix = '.uld'
    fname_out_suffix = '.csv'

    for item in sys.argv[1:]:
        if item.startswith('-path='):
            path = item.partition('=')[2]
        if item.startswith('-prefix='):
            fname_prefix = item.partition('=')[2]
        if item.startswith('-trade_matrix='):
            TradePosition.MATRIX_SIZE = int(item.partition('=')[2])


    run = Run()
    run.start(path, fname_prefix)
