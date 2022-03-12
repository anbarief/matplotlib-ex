"""
Author: Arief Anbiya
Email: anbarief@live.com
Date: 3 Sept 2020
The dataset used is the Average Interest Rates from US Treasury Securities, collected from:
https://fiscaldata.treasury.gov/datasets/average-interest-rates-treasury-securities/
The run_animation function shows animation of the dynamics of the Average Interest Rates of each security type.
DATASET FILE: "average_interest_rates_US_treasury.csv"
"""

import math

import pandas
import matplotlib.pyplot as plt
import matplotlib.animation as animation

FILE_PATH = "average_interest_rates_US_treasury.csv"

df = pandas.read_csv(FILE_PATH)
n = len(df)
description = list(df['Security Description'])
for i in range(n):
    if description[i] == "Treasury Floating Rate Note(FRN)":
       description[i] =  "Treasury Floating Rate Note (FRN)"
    if description[i] == "Treasury Inflation-Protected Securities(TIPS)":
       description[i] =  "Treasury Inflation-Protected Securities (TIPS)"
    if description[i] == "TotalMarketable":
       description[i] =  "Total Marketable"
df['Security Description'] = description       

def run_animation(interval_between_frame=100):
    
    security_description = sorted(list(set(df['Security Description'])))
    n_security = len(security_description)

    time_points = [int(i.split('-')[0]) + int(i.split('-')[1])/12 + int(i.split('-')[2])/(31*12) \
                  for i in df['Record Date']]
    df['Time Point'] = time_points
    unique_time_points = sorted(list(set(time_points)))
    n_unique_t = len(unique_time_points)

    fig, ax = plt.subplots()
    fig.set_tight_layout(True)

    def animate(frame):
        ax.cla()
        
        df1=df[df['Time Point']==unique_time_points[frame]]
        interest_rate = []
        bars=[]
        count = 0

        for i in security_description:
            df2 = df1[df1['Security Description']==i]['Average Interest Rate Amount']
            if len(df2)==0:
                interest_rate.append(0)
            else:
                interest_rate.append(df2[df2.index[0]])
            info = df1[df1['Security Description']==i]['Security Type Description']
            if len(info)!=0:
                info = info[info.index[0]]
            else:
                info =""
            if info == 'Marketable':
                color = (0,0,1,1)
            elif info == 'Non-marketable':
                color = (1,0,0,1)
            else:
                color = (0,0,0,1)
            bar=ax.bar(count, interest_rate[-1], color = color)
            bars.append(bar[0])
            count+=1

        ax.set_ylim([0, 10])
        ax.set_xlim([-1, n_security+1])
        ax.set_xticks(range(n_security))
        ax.set_xticklabels(security_description, rotation = -90, fontsize = 6)
        ax.set_yticks([2, 4, 6, 8, 10])
        ax.set_yticklabels(['2%', '4%', '6%', '8%', '10%'])
        ax.set_title(list(df1['Record Date'])[0])
        ax.set_ylabel("Average Interest Rate")
        
        return bars    

    ani = animation.FuncAnimation(fig, animate, n_unique_t, repeat=False, interval=interval_between_frame)
    
    plt.show()

run_animation()
