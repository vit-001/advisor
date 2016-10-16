# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator, \
    DayLocator, MONDAY
from matplotlib.finance import quotes_historical_yahoo_ohlc, candlestick2_ohlc


CSin = list((
1.13359, 1.13343, -1,1.13338, 1.13347, 1.1336, 1.13362, 1.13373, 1.13399, 1.13388, 1.13391, 1.13367, 1.1336, 1.13364,
1.13374, 1.13397, 1.13383, 1.13335, 1.13352, 1.13366, 1.13314, 1.13306, 1.13291, 1.1329, 1.13289, 1.13289, 1.13279,
1.13301, 1.13277, 1.13279, 1.13282, 1.13291, 1.13301, 1.13319, 1.13319, 1.13322, 1.13338, 1.13303, 1.13289, 1.13295,
1.1328, 1.1329, 1.13288, 1.133, 1.1328, 1.1325, 1.13229, 1.13188, 1.13228, 1.13198, 1.13202))

CSmax = list((
1.13359, 1.13353, -1,1.13349, 1.13359, 1.1337, 1.13372, 1.134, 1.13403, 1.13393, 1.13402, 1.13369, 1.13369, 1.13378,
1.13402, 1.13397, 1.13383, 1.13378, 1.13368, 1.13373, 1.13337, 1.1333, 1.13298, 1.13309, 1.13294, 1.13291, 1.13322,
1.13306, 1.13285, 1.13283, 1.13294, 1.13304, 1.13343, 1.13322, 1.13324, 1.13336, 1.13339, 1.13304, 1.133, 1.13297,
1.13289, 1.13301, 1.13301, 1.13304, 1.1328, 1.13251, 1.1323, 1.13232, 1.13234, 1.13203, 1.13232))

CSmin = list((
1.13342, 1.13327, -1,1.13336, 1.13345, 1.13352, 1.1336, 1.13363, 1.13384, 1.13385, 1.13366, 1.13351, 1.13348, 1.13359,
1.13374, 1.13382, 1.13338, 1.13332, 1.13346, 1.13313, 1.13297, 1.13289, 1.13288, 1.13287, 1.13277, 1.13276, 1.13279,
1.13278, 1.13257, 1.13264, 1.13281, 1.13289, 1.13293, 1.1331, 1.13317, 1.13316, 1.13307, 1.13282, 1.13286, 1.13269,
1.1328, 1.13289, 1.13288, 1.13285, 1.13248, 1.13227, 1.13173, 1.13188, 1.13196, 1.13189, 1.13193))

CSout = list((
1.13343, 1.13339, -1,1.13349, 1.13359, 1.13363, 1.13372, 1.13398, 1.13387, 1.13391, 1.13366, 1.13359, 1.13367, 1.13373,
1.13398, 1.13384, 1.1334, 1.13349, 1.13368, 1.13314, 1.13307, 1.1329, 1.13291, 1.13288, 1.13289, 1.13283, 1.133,
1.13278, 1.13278, 1.13283, 1.13292, 1.133, 1.1332, 1.13318, 1.13321, 1.13335, 1.13307, 1.1329, 1.13296, 1.13278,
1.13289, 1.1329, 1.13301, 1.13285, 1.13252, 1.13228, 1.13189, 1.13227, 1.13196, 1.132, 1.13223))


# # (Year, month, day) tuples suffice as args for quotes_historical_yahoo
# date1 = (2004, 2, 1)
# date2 = (2004, 4, 12)
#
# mondays = WeekdayLocator(MONDAY)  # major ticks on the mondays
# alldays = DayLocator()  # minor ticks on the days
# weekFormatter = DateFormatter('%b %d')  # e.g., Jan 12
# dayFormatter = DateFormatter('%d')  # e.g., 12
#
# quotes = quotes_historical_yahoo_ohlc('INTC', date1, date2)
# if len(quotes) == 0:
#     raise SystemExit

# fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
f = plt.figure()
plt.subplots_adjust(hspace=0.001)




# fig, ax = plt.subplots()
# fig.subplots_adjust(bottom=0.2)

# ax.xaxis.set_major_locator(mondays)
# ax.xaxis.set_minor_locator(alldays)
# ax.xaxis.set_major_formatter(weekFormatter)
# ax.xaxis.set_minor_formatter(dayFormatter)

#plot_day_summary(ax, quotes, ticksize=3)

ax1 = plt.subplot(211)
candlestick2_ohlc(ax1, CSin, CSmax, CSmin,CSout, width=0.8)

ax2 = plt.subplot(212, sharex=ax1)
CSmax[2]=None
CSmin[2]=None
ax2.plot(CSmax)
ax2.plot(CSmin)

# plt.tight_layout()

# ax.xaxis_date()
# ax.autoscale_view()
# plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

plt.show()