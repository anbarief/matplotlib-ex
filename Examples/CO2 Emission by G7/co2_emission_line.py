import matplotlib.pyplot as plt
from matplotlib import font_manager
import pandas

helvetica = font_manager.FontProperties(fname = "HelveticaNeueBold.ttf", size = 15)

def get_value(nation, year):
    nation_df = df[df['Entity']==nation]
    nation_df_in_year = nation_df[nation_df['Year']==year]
    return list(nation_df_in_year['Annual CO2 emissions (per capita)'])[0]

df = pandas.read_csv('co-emissions-per-capita.csv')

years = range(1970, 2021)
n_years = len(years)

g_seven = {'United Kingdom': {'color': (0, 0, 0, 0.6), \
                              'data': [(i, get_value('United Kingdom', i)) for i in years]}, \
           'Japan': {'color': (1,0,0,0.6), \
                     'data': [(i, get_value('Japan', i)) for i in years]}, \
           'Italy': {'color': (0,1,0,0.6), \
                     'data': [(i, get_value('Italy', i)) for i in years]}, \
           'Canada': {'color': (1, 0.5, 0, 0.6), \
                      'data': [(i, get_value('Canada', i)) for i in years]}, \
           'EU-28': {'color': (0,0,1,0.6), \
                     'data': [(i, get_value('EU-28', i)) for i in years]}, \
           'United States': {'color': (150/255,0,64/255, 0.6), \
                             'data': [(i, get_value('United States', i)) for i in years]}, \
           'Germany': {'color': (0,1,1,0.6), \
                       'data': [(i, get_value('Germany', i)) for i in years]}}

fig, ax = plt.subplots()
ax.axis('off')
ax.set_ylim([-6, 25])

for i in range(n_years):
    if (i%5 == 0):
        ax.text(years[i], -5, str(years[i]), ha='center', va = 'center', color='black', fontsize=10)

ax.text(years[0]-2.5, 0, "0", color='black', fontsize=20, ha = 'center', va = 'center')
ax.text(years[0]-2.5, 20, "20t", color='black', fontsize=20, ha = 'center', va = 'center') 
ax.text(1965, 24, r'G7 countries Annual $CO_2$ emissions (per capita)', fontproperties = helvetica)
ax.text(years[0]+20, 0, "*data from: https://ourworldindata.org/co2-and-other-greenhouse-gas-emissions", fontstyle='italic', fontsize=8)

legend_names = []
for nation in g_seven.keys():
    time = [i[0] for i in g_seven[nation]['data']]
    value = [i[1] for i in g_seven[nation]['data']]
    ax.plot(time, value, '-', color =  g_seven[nation]['color'], lw=4)
    legend_names.append(nation)
ax.legend(legend_names, ncol = 2, bbox_to_anchor = (0.6, 0.87), edgecolor = 'black', borderpad=1, shadow=True)

fig.set_facecolor('white')
fig.set_size_inches(10, 6)
fig.show()
