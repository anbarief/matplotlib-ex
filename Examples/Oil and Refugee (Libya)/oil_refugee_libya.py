#author: Arief Anbiya (2022)
#e-mail: anbarief@live.com

import matplotlib.pyplot as plt
from matplotlib import font_manager
import pandas

lato_light = font_manager.FontProperties(fname = "Lato-Light.ttf", size = 17)
lato_light_medium = font_manager.FontProperties(fname = "Lato-Light.ttf", size = 15)
lato_light_small = font_manager.FontProperties(fname = "Lato-Light.ttf", size = 11)
lato_light_smaller = font_manager.FontProperties(fname = "Lato-Light.ttf", size = 10)

df = pandas.read_csv('refugee-population-by-country-or-territory-of-origin.csv')
df2 =  pandas.read_csv('oil-prod-per-capita.csv')

libya = df[df['Entity'] == 'Libya']
year = libya['Year']
refugee = libya['Refugee population by country or territory of origin']
minmax=min(refugee), max(refugee)

libya2 = df2[df2['Entity'] == 'Libya']
index = libya2.index[0]
while (min(libya2['Year']) != 1980):
    libya2 = libya2.drop(index)
    index+=1
year2 = libya2['Year']
oil_production = libya2['Oil production per capita (kWh)']
minmax2=min(oil_production), max(oil_production)

fig, ax = plt.subplots()

ax.fill_between(year2, oil_production, '-', color = (1,0.5,0,0.3), zorder=0)
ax.set_title('Libya refugee population (right) \n and \n Oil production per capita (left)', fontproperties=lato_light)
ax.set_xticks(year)
ax.set_xticklabels([str(i) for i in year], rotation = 90, fontproperties=lato_light_small, color='black')
ax.set_yticks(minmax2)
ax.set_yticklabels(["34,565.37\nkWh", "318,457.2\nkWh"], fontproperties=lato_light_medium)
ax.legend(['Oil production'], prop=lato_light_smaller, \
          bbox_to_anchor = [0.3,0.77], loc = 'lower left')

ax2 =ax.twinx()
ax2.plot(year, refugee, '-', color = (0.1,0.1,0.1,1), lw = 3)
ax2.plot([year[4208], year[4209], year[4210]], \
        [refugee[4208], refugee[4209], refugee[4210]], \
        '-', color = 'red', lw=3)

ax2.set_yticks(minmax)
ax2.set_yticklabels(["205\npeople", "17,595\npeople"], fontproperties=lato_light_medium)
ax2.legend(['No. of refugees','No. of refugees (around NATO intervention)'], prop=lato_light_smaller, \
           bbox_to_anchor = [0.3,0.85], loc = 'lower left')

quote = "What is the reason for the invasion of Iraq and the killing of millions of people?\n\
Let our American friends answer this question for us. Why Iraq? What is the reason? Was Bin Laden Iraqi?\n\
No it wasn't. Were those who shot New York Iraqi? No they weren't!\n\
Were there any chemical WMD in Iraq? Did not have!\nEven if Iraq had chemical weapons,\n\
states like Pakistan, India, America, France, England, Russia have nuclear bombs!\n-Muammar Gaddafi (former President of Libya)"
ax.text(1980.2, 34600, quote, fontproperties = lato_light_small)
ax.text(2005, 200000, "NATO intervention in 2011, bombing, \nwhich killed Gaddafi and civillians.", fontproperties=lato_light_small)
ax.arrow(2010.5, 199000, 0, -130000, color='gray')
ax.set_xlim([1978, 2022])

fig.show()
