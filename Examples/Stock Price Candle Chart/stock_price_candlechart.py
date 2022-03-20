#Author: Arief Anbiya (2022)
#E-mail: anbarief@live.com

import statistics
mean = statistics.mean
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

#function to generate candle object (Rectangle object) for each trading day
def candle_obj(open_price, close_price, x_pos):
    width = 0.3
    diff = close_price - open_price
    if diff >= 0:
        color = 'green'
    else:
        color = 'red'
    candle = Rectangle([x_pos-width, min(close_price, open_price)], 0.6, abs(diff), color = color)
    return candle

def plot_day(ax, x_pos, open_price, close_price, high, low):
    candle_patch = candle_obj(open_price, close_price, x_pos)
    ax.plot([x_pos, x_pos], [low, high], '-', lw = 1, color = 'black', zorder=0)
    ax.add_patch(candle_patch)
   
def exponential_smoothing(data, a=1):
    result = [data[0]]
    for i in data[1:]:
        result.append( a*i + (1-a)*result[-1] )
    return result

def moving_average(data, n=5):
    N=len(data)
    return range(n-1, N), [mean(data[i:i+n]) for i in range(N-(n-1))]
    
fig, ax = plt.subplots()

#take most recent 999 price
data1 = pd.read_csv('BBRI.JK.csv')
date1 = list(data1['Date'].dropna())[-1000:-1]
open1 = list(data1['Open'].dropna())[-1000:-1]
close1 = list(data1['Close'].dropna())[-1000:-1]
high1 = list(data1['High'].dropna())[-1000:-1]
low1 = list(data1['Low'].dropna())[-1000:-1]
n1 = len(close1)
x_mav, mav = moving_average(close1, n=7)

#Plot candle and MAV for data1:
for i in range(n1):
    plot_day(ax, i, open1[i], close1[i], high1[i], low1[i])

line = ax.plot(x_mav, mav, '-', color = (0, 0, 1, 0.5), lw=1)[0]
ax.legend([line], ['7-day moving average (close price)'])
ax.set_xlim([n1-30-2, n1+2])
ax.set_ylim([min(low1[n1-30:])*0.95, 1.05*max(high1[n1-30:])])
ax.set_title("OHLC candle chart plot", fontweight='bold', style='italic')
ax.set_xlabel("Day-0, {} \n until Day-{}, {}".format(date1[0], n1-1, date1[-2]), style='italic', fontsize=8)
ax.set_ylabel("BBRI Stock Price", fontweight='bold')

plt.tight_layout()

figsize = fig.get_size_inches()
fig.set_size_inches([figsize[0], figsize[1]*1.25])
fig.show()
