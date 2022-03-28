#Author: Arief Anbiya (2019)
#E-mail: anbarief@live.com

import random
import copy
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import Rectangle
from matplotlib.patches import Circle
import pandas


helv = fm.FontProperties(fname = "HelveticaNeueBold.ttf", \
                  size = 20, weight = 'heavy')
helv_country_name = fm.FontProperties(fname = "HelveticaNeueBold.ttf", \
                  size = 10, weight = 'heavy')
helvSmall = fm.FontProperties(fname = "HelveticaNeueBold.ttf", \
                  size = 15, weight = 'heavy')
helvMed = fm.FontProperties(fname = "HelveticaNeueBold.ttf", \
                  size = 40, weight = 'heavy')
helvBig = fm.FontProperties(fname = "HelveticaNeueBold.ttf", \
                  size = 100, weight = 'heavy')


def draw_random_vline(ax, xlim, ylim, color, lw):
    x_start = random.uniform(xlim[0], xlim[1])
    start_pos = [x_start, ylim[0]]
    gradient = 0.1
    while start_pos[1] < ylim[1]:
        col = [gradient*color[0], gradient*color[1], gradient*color[2], color[3]]
        gradient += 0.1
        h = random.uniform( -(x_start - xlim[0]), (xlim[1] - x_start))
        v = random.uniform(0, (ylim[1]-ylim[0])/10)
        if start_pos[1]+v <= ylim[1]:
            ax.plot([start_pos[0], start_pos[0]+h], [start_pos[1], start_pos[1]+v], '-', \
                color = col, lw = lw)
        x_start = start_pos[0]+h
        start_pos = [x_start, start_pos[1]+v]
    
def continent(country):
    africa = ["Botswana", "Central African Republic", "Comoros", \
              "Congo, Republic of", "Djibouti", "Equatorial Guinea", \
              "Gabon", "Gambia", "Guinea-Bissau", "Namibia", \
              "Lesotho", "Liberia", "Mauritania", "Mauritius", \
              "São Tomé and Príncipe", "Seychelles", \
              "Cabo Verde", "Eswatini"]
    asia = ["Armenia", "Bahrain", "Bhutan", "Brunei Darussalam", "Cyprus", "Georgia", \
            "Kuwait", "Lebanon", "Maldives", "Mongolia", "Oman", "Qatar", \
            "Timor-Leste"]
    americas = ["Bahamas", "Barbados", "Belize", "Costa Rica", "Guyana", \
               "Dominica", "Jamaica", "Panama", "Saint Lucia", \
               "Saint Vincent and the Grenadines", "Trinidad and Tobago", \
               "Suriname", "Uruguay"]
    oceania = ["Vanuatu", "New Zealand", "Samoa", "Solomon Islands", "Tonga", \
               "Fiji","Kiribati", "Micronesia"]
    europe = ["Bosnia and Herzegovina", "Croatia", "Estonia", \
              "Iceland", "Ireland", "Kosovo", "Latvia", \
              "Lithuania", "Luxembourg", "Macedonia", "Malta", \
              "Moldova", "Montenegro", "Slovenia", "Albania"]
    if country in africa:
        return "Africa"
    elif country in asia:
        return "Asia"
    elif country in americas:
        return "Americas"
    elif country in oceania:
        return "Oceania"
    else:
        return "Europe"
    
continentColor = {"Africa": [0, 0.5, 0, 1], \
                   "Asia": [0, 0, 1, 1], \
                   "Americas": [1, 1, 0, 1], \
                   "Oceania": [0, 0.7, 0.7, 1], \
                   "Europe": [1, 0, 0, 1]}

################################################################

## Questions:
## -What are the trends? OK
## Use Land Area as square, the Population as the color density
## -What is the link between the Diaspora and other indexes? OK
## -.....

address = "WDVP-Datasets.csv"
dataFrame = pandas.read_csv(address)
dataFrame = dataFrame.rename(index=str, columns = {"indicator": "country", \
                                                   "GDP ":"GDP(billions)"})

address2 = "index2018_data.csv"
index2018df = pandas.read_csv(address2)

eswatini = {'BusinessF': 61.1, 'LaborF': 69.5, 'MonetaryF': 73.2, \
            'TradeF': 79.7, 'InvestF': 50, 'FinanceF': 40}

businessF = []
laborF = []
monetaryF = []
tradeF = []
investF = []
financeF = []
for i in range(len(dataFrame)):
    business = 0
    labor = 0
    monetary = 0
    trade = 0
    invest  = 0
    finance = 0
    if dataFrame['country'][i] == "Eswatini":
            business = eswatini['BusinessF']
            labor = eswatini['LaborF']
            monetary = eswatini['MonetaryF']
            trade = eswatini['TradeF']
            invest  = eswatini['InvestF']
            finance = eswatini['FinanceF']
    else:
        for j in range(len(index2018df)):
            if dataFrame['country'][i] == index2018df['Country Name'][j]:
                business = index2018df['Business Freedom'][j]
                labor = index2018df['Labor Freedom'][j]
                monetary = index2018df['Monetary Freedom'][j]
                trade = index2018df['Trade Freedom'][j]
                invest  = index2018df['Investment Freedom '][j]
                finance = index2018df['Financial Freedom'][j]
                break
    businessF.append(business)
    laborF.append(labor)
    monetaryF.append(monetary)
    tradeF.append(trade)
    investF.append(invest)
    financeF.append(finance)

dataFrame = dataFrame.assign(BusinessF = businessF, LaborF = laborF, FinanceF = financeF, \
                 MonetaryF = monetaryF, TradeF = tradeF, InvestF = investF)

maxGDPbil = max([float(i) for i in dataFrame['GDP(billions)'][4:]])
n = len(dataFrame['country'][4:])
overallGDP = []
#########################################################################3

class IndexRectangle:
    def __init__(self, nation, value, color):
        self.nation = nation
        self.value = value
        self.color = color
    def plot(self, ax, xy, width, height):
        self.patch = Rectangle(xy, width, height, color = self.color, linewidth = 3, ec = self.color[0:3] + [1])
        ax.add_patch(self.patch)


class Square:
    def __init__(self, nation, value, color):
        self.nation = nation
        self.value = value 
        self.color = color
    def plot(self, ax, xy, width, height):
        self.patch = Rectangle(xy, width, height, color = self.color, ec = (0,0,0,0))
        ax.add_patch(self.patch)

class Nation:
    def __init__(self, name, continent, population, landarea, hdi, **kwargs):
        self.name = name
        self.continent = continent
        self.population = population
        self.landarea = landarea
        self.pplSquares = int(population/10000)
        self.hdi = hdi
        self.diaspora = kwargs['diaspora']
        self.dias_ratio = self.diaspora/self.population
        self.businessF = kwargs['businessF']
        self.laborF = kwargs['laborF']
        self.financeF = kwargs['financeF']
        self.monetaryF = kwargs['monetaryF']
        self.tradeF = kwargs['tradeF']
        self.investF = kwargs['investF']
        self.gdp = kwargs['gdp']

        self.color = continentColor[self.continent][0:3] + [0.9*min((self.population/self.landarea)/100, 1) + 0.1]

    def addLabel(self, ax, xy, **kwargs):
        ax.text(*xy, self.name, kwargs)
        

###############################################
nations = []
for i in range(n):
    country = dataFrame["country"][i+4]
    population = float(dataFrame["population"][i+4].replace(",", ""))
    landArea = float(dataFrame["land area (sq km)"][i+4].replace(",", ""))
    hdi = float(dataFrame["human development index"][i+4].replace("-", "0"))
    diaspora = float(dataFrame["population living abroad (diaspora)"][i+4].replace("-", "0"))
    business = dataFrame["BusinessF"][i+4]
    labor = dataFrame["LaborF"][i+4]
    trade = dataFrame["TradeF"][i+4]
    invest = dataFrame["InvestF"][i+4]
    monetary = dataFrame["MonetaryF"][i+4]
    finance = dataFrame["FinanceF"][i+4]
    gdp = float(dataFrame["GDP(billions)"][i+4])
    nation = Nation(country, \
                    continent(country), \
                    population, \
                    landArea, \
                    hdi, \
                    diaspora = diaspora, \
                    businessF = business, \
                    laborF = labor, \
                    tradeF = trade, \
                    investF = invest, \
                    monetaryF = monetary, \
                    financeF = finance, \
                    gdp = gdp)
    
    nation._population_str = dataFrame["population"][i+4]
    nation._landArea_str = dataFrame["land area (sq km)"][i+4]
    nations.append(nation)

sortbyDias = sorted(nations, key = lambda x: x.dias_ratio, reverse = True)
sortbyGDP = list(sorted(sortbyDias, key = lambda x:x.gdp))
maxGDP = max([i.gdp for i in sortbyDias])

#########################################
#########################################
#########################################
#########################################
#########################################
#########################################
#########################################
#########################################
#########################################

fig, ax = plt.subplots()

silver = [196/255, 199/255, 206/255, 0.8]
ax.set_fc(silver)

ax.axis('equal')

ax.text(0, -120, "Small Countries with Squares", \
        ha = 'center', va = 'center', fontproperties = helvBig)

comment = "Data source timeline"
ax.plot([-400, -200], [-180, -180], \
        '-', lw = 6, color = 'black')

ax.text(-400, -183, "2015", rotation = -90, \
        ha = 'center', va = 'top', fontproperties = helvMed)
ax.text(-400, -180+5, "Population living abroad (diaspora) data year:\n\
(https://wdvp.worldgovernmentsummit.org/assets/downloads/WDVP-Datasets.xlsx)", \
        fontproperties = helv, ha = 'center', va = 'bottom', rotation = -90)

ax.text(-400 + 2*50, -183, "2017", rotation = -90, \
        ha = 'center', va = 'top', fontproperties = helvMed)
ax.text(-400 + 2*50, -180+5, "Human development index data year:\n\
(https://wdvp.worldgovernmentsummit.org/assets/downloads/WDVP-Datasets.xlsx)", \
        fontproperties = helv, ha = 'center', va = 'bottom', rotation = -90)

ax.text(-400 + 3*50, -183, "2018", rotation = -90, \
        ha = 'center', va = 'top', fontproperties = helvMed)
ax.text(-400 + 3*50, -180+5, "Population, land area, GDP, \nand Economic Freedom index data year:\n\
(https://www.heritage.org/index/explore)", \
        fontproperties = helv, ha = 'center', va = 'bottom', rotation = -90)

ax.text(290, -180, "Author: Arief Anbiya", \
        ha = 'center', va = 'center', style = "italic", fontproperties = helvMed, color = [0,0,0,0.5])

comment = "SQUAREEEEEEEEEEEEEEEEEEEEEEES"
totalPpl = sum([i.population for i in sortbyDias])

squares = []
for i in sortbyDias:
    nsquares = int(i.population/10000)
    for j in range(nsquares):
        squares.append(Square(i, 10000, i.color))

copySquares = copy.deepcopy(squares)
orderedSquares = []
for i in range(len(squares)):
    picked = random.choice(copySquares)
    orderedSquares.append(picked)
    copySquares.remove(picked)

### PLOT SQUARES
xy = [-270, 0]
for i in range(len(orderedSquares)):
    orderedSquares[i].plot(ax, xy, 2, 2)
    if (i+1)%100 == 0:
        xy = [-270, xy[1]+2.5]
    else:
        xy = [xy[0]+2.5, xy[1]]
        
### SQUARES for POPULATION (sorted per CONTINENT)
sortedsquareContinent = list(sorted(squares, key = lambda x: x.nation.continent))
xy = [20, 0]
for i in range(len(sortedsquareContinent)):
    sortedsquareContinent[i].plot(ax, xy, 2, 2)
    if (i+1)%100 == 0:
        xy = [20, xy[1]+2.5]
    else:
        xy = [xy[0]+2.5, xy[1]]


comment = "Land Area squares"
initialY = xy[1] + 25
totalscaleLand = sum([i.landarea/35000 for i in sortbyDias])
maxscaleLand = max([i.landarea/35000 for i in sortbyDias])
xy = [0 - 0.5*(totalscaleLand + 3*70), xy[1] + 25]
for i in sortbyDias:
    patch = Rectangle(xy, i.landarea/35000, i.landarea/35000, \
                      color = i.color)
    i.landPatch = patch
    ax.add_patch(patch)
    if (i.landarea/35000 >= 0.5*maxscaleLand):
        ax.text(xy[0] + 0.5*i.landarea/35000, xy[1]-10, \
                i._landArea_str+ "\n" +r"land area ($km^2$)", \
                ha = 'center', va = 'center', fontproperties = helv, \
                color = [0.2, 0.2, 0.2, 0.8])
    xy = [xy[0] + i.landarea/35000 + 3, xy[1]]

maxY = xy[1] + maxscaleLand + 50
xyLabel = [0 -35*10, maxY + 18]
for i in sortbyDias:
    ax.plot([xyLabel[0], i.landPatch.xy[0]], \
            [xyLabel[1]-5-25, i.landPatch.xy[1]], \
            '-', color = i.color[0:3] + [0.3], lw = 0.1)
    xyLabel = [xyLabel[0] + 10, xyLabel[1]]


comment = "How to read the chart"
ax.text(-145, -30, ". Randomized version of the population squares: not ordered by continent.", \
        fontproperties = helv, \
        bbox ={'boxstyle':'round', 'fc': (0,0,0,0), 'ec': "brown", 'pad':1.2, 'linewidth': 2}, \
        va = 'top', ha = 'center', color = "brown")

ax.text(-145, -10, ". Overall population: 125,500,000"+"\n"\
                   +". Overall squares: 12,550", \
        ha = 'center', va = 'center', color = [0.2, 0.2, 0.2, 0.8], fontproperties = helv)

ax.text(145, -30, ". The squares represent the population of all the small countries.\n\
. Each square represents 10,000 people.\n\
. They are stacked per continent.\n\
. Africa has the largest population (35,500,000)", \
        fontproperties = helv, \
        bbox ={'boxstyle':'round', 'fc': (0,0,0,0), 'ec': "brown", 'pad':1.2, 'linewidth': 2}, \
        va = 'top', ha = 'center', color = "brown")

ax.text(-35*10, maxY + 56, "The country names are sorted by the diaspora proportion", \
        fontproperties = helv, bbox ={'boxstyle':'round', 'fc': (0,0,0,0), 'ec': "brown", 'pad':0.5, 'linewidth': 2}, \
        va = 'top', ha = 'left', color = "brown")

ax.plot([-35*10, -35*10 + 80], [maxY + 70, maxY + 70], '-', \
        color = "black", lw = 4)
ax.text(-35*10 + 40, maxY + 77, "Total population living abroad (diaspora)", \
        fontproperties = helv, color = "black", ha = 'center', va = 'center')
ax.text(-35*10 + 40, maxY + 65, "Total population", \
        fontproperties = helv, color = "black", ha = 'center', va = 'center') 

for i in range(len(sortbyDias)):
    maxRect = Rectangle([-35*10 + i*10, maxY + 39], 8, 2, color = (0,0,0,0), ec = "black" ,lw = 3)
    ax.add_patch(maxRect)


indexName = ["GDP(billions)", "Human Dev. Index", \
             "Business Freedom", "Labor Freedom", \
             "Trade Freedom", "Financial Freedom"] 

qatarObj = [i for i in sortbyDias if i.name == "Qatar"][0]    

qatarIdx = [1, qatarObj.hdi, qatarObj.businessF/100, qatarObj.laborF/100, \
            qatarObj.tradeF/100, qatarObj.financeF/100]

rect = Rectangle([-35*10 + 210, maxY + 50], 24, 6, \
                 color = qatarObj.color, ec = "black" ,lw = 3)
ax.text(-35*10 + 205, maxY + 50 + 3, indexName[0], \
            ha = 'right', va = 'center', \
            fontproperties = helv, color = "black")
ax.text(-35*10 + 210 + 29, maxY + 50 + 3, " <---- Max. length bar, Qatar has the highest GDP (329.2 billions)", \
            ha = 'left', va = 'center', \
            fontproperties = helv, color = "black")
ax.add_patch(rect)

for i in range(1, 6):
    rect = Rectangle([-35*10 + 210, maxY + 50 + 10 + 6*i], 24*(qatarIdx[i]), 6, \
                     color = qatarObj.color , linewidth = 3, ec = qatarObj.color[0:3] + [1])
    ax.text(-35*10 + 205, maxY + 50 + 10 + 6*i + 3, indexName[i], \
            ha = 'right', va = 'center', \
            fontproperties = helv, color = "black")
    ax.add_patch(rect)

ax.text(-35*10 + 210 + 12, maxY + 50 + 3 + 10 + 6*6 + 2, \
        "Using enlarged Qatar index and GDP bars as an example:", \
            ha = 'center', va = 'center', \
            fontproperties = helv, color = "black")

ax.text(-35*10 + 210 + 29, maxY + 50 + 3 + 10 + 6*3, " <---- Highest value can be up to 100 for max. length bar", \
            ha = 'left', va = 'center', \
            fontproperties = helv, color = "black")

comment = "Country labels"
xy = [0 -35*10, maxY + 18]
ax.plot(2*[xy[0]- 7], [xy[1], xy[1] - 25], '-', lw = 3, color = 'black')
ax.plot([xy[0]- 10, xy[0] - 4], [xy[1], xy[1]], '-', lw = 3, color = 'black')
ax.plot([xy[0]- 10, xy[0] - 4], [xy[1]-25, xy[1]-25], '-', lw = 3, color = 'black')
ax.text(xy[0]-13, xy[1] - 12.5, "Diaspora proportion\n100%", ha = 'center', va ='center', rotation = 90, \
        color = 'black', size = 20, fontproperties = helv)

comment = "DIASPORA LINE"
for i in sortbyDias:
    for j in range(5):
        draw_random_vline(ax, [xy[0], xy[0] + 6], [xy[1] - 25*i.dias_ratio, xy[1]], \
                          color = [0.2, 0.2, 0.2, 1], lw = 2)
    ax.plot([xy[0] + 1, xy[0]+1], [xy[1], xy[1] - 25], '--', color = 'gray', \
            lw = 2)
    i.addLabel(ax, [xy[0], xy[1] - 5 - 60], \
               color = 'black', fontproperties = helv_country_name, rotation = -90)
               #bbox = {'boxstyle':'round', 'facecolor': 'none', \
               #        'edgecolor': i.color[0:3] + [1], 'linewidth':5})
    xy = [xy[0] + 10, xy[1]]

comment = "RECTANGLES OF ECONOMIC FREEDOM"

gdpRects = []
for i in sortbyDias:
    gdpRects.append( IndexRectangle(i, 8*i.gdp/maxGDP, i.color) )
    
hdiRects = []   
for i in sortbyDias:
    hdiRects.append( IndexRectangle(i, 8*i.hdi, i.color) )

businessRects = []
for i in sortbyDias:
    businessRects.append( IndexRectangle(i, 8*i.businessF/100, i.color) )

laborRects = []
for i in sortbyDias:
    laborRects.append( IndexRectangle(i, 8*i.laborF/100, i.color) )

tradeRects = []
for i in sortbyDias:
    tradeRects.append( IndexRectangle(i, 8*i.tradeF/100, i.color) )

financeRects = []
for i in sortbyDias:
    financeRects.append( IndexRectangle(i, 8*i.financeF/100, i.color) )

xy = [0 -35*10, maxY + 20]
for i in gdpRects:
    i.plot(ax, xy, i.value, 2)
    xy = [xy[0] + 10, xy[1]]
xy = [0 -35*10, maxY + 20 + 7]
for i in hdiRects:
    i.plot(ax, xy, i.value, 2)
    xy = [xy[0] + 10, xy[1]]
xy = [0 -35*10, maxY + 20 + 9]
for i in businessRects:
    i.plot(ax, xy, i.value, 2)
    xy = [xy[0] + 10, xy[1]]
xy = [0 -35*10, maxY + 20 + 11]
for i in laborRects:
    i.plot(ax, xy, i.value, 2)
    xy = [xy[0] + 10, xy[1]]
xy = [0 -35*10, maxY + 20 + 13]
for i in tradeRects:
    i.plot(ax, xy, i.value, 2)
    xy = [xy[0] + 10, xy[1]]
xy = [0 -35*10, maxY + 20 + 15]
for i in financeRects:
    i.plot(ax, xy, i.value, 2)
    xy = [xy[0] + 10, xy[1]]

for i in range(20):
    africaRect = Rectangle([160, maxY + 53 + 3*i], 20, 3, color = [0,0.5,0,i/19], \
                         ec = [0,0,0, 0])
    ax.add_patch(africaRect)

    asiaRect = Rectangle([180, maxY + 53 + 3*i], 20, 3, color = [0,0,1,i/19], \
                         ec = (0,0,0,0))
    ax.add_patch(asiaRect)

    oceaniaRect = Rectangle([200, maxY + 53 + 3*i], 20, 3, color = [0,0.7,0.7,i/19], \
                            ec = (0,0,0,0))
    ax.add_patch(oceaniaRect)

    americasRect = Rectangle([220, maxY + 53 + 3*i], 20, 3, color = [1,1,0,i/19], \
                            ec = (0,0,0,0))
    ax.add_patch(americasRect)

    europeRect = Rectangle([240, maxY + 53 + 3*i], 20, 3, color = [1,0,0,i/19], \
                            ec = (0,0,0,0))
    ax.add_patch(europeRect)

ax.text(150, maxY + 53 + 3*19, "Solid color means country \n"+\
r"with at least 100 people per $1 km^2$ land area." + "\n" + \
"More transparent color means \n" + r"less populated country per $1 km^2$ land area", \
        fontproperties = helv, ha = 'right', va = 'top', \
        bbox ={'boxstyle':'round', 'fc': (0,0,0,0), 'ec': "brown", 'pad':1.2, 'linewidth': 2}, \
        color = "brown")


ax.set_xlim([0 - 450, 0 + 400])
ax.set_ylim([-100, 500])
ax.tick_params(colors = (0,0,0,0))

forLegend = [\
    ax.plot(-1000, 1000, color = continentColor['Africa'], lw = 20)[0],\
    ax.plot(-1000, 1000, color = continentColor['Asia'], lw = 20)[0],\
    ax.plot(-1000, 1000, color = continentColor['Oceania'], lw = 20)[0],\
    ax.plot(-1000, 1000, color = continentColor['Americas'], lw = 20)[0],\
    ax.plot(-1000, 1000, color = continentColor['Europe'], lw = 20)[0]
    ]
ax.legend(forLegend, ['Africa', 'Asia', 'Oceania', 'Americas', 'Europe'], \
          prop = helvMed, ncol = 5)

fig.set_size_inches(60, 60)
fig.savefig('wdvp_squares.pdf', dpi = 'figure')    
