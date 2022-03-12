#Copyright Arief Anbiya (2022)
#E-mail: anbarief@live.com

import statistics

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

sofia_regular_otf = "Sofia-Regular.otf"
sofia_regular = fm.FontProperties(fname = sofia_regular_otf, size = 10)

def num2digits(number, descend=True):
    strnum = str(number)
    while len(strnum) < 4:
        strnum = '0' + strnum
    return sorted([int(i) for i in str(strnum)], reverse=descend)

def digits2num(digits):
    return int(''.join([str(i) for i in digits]))

def make_pair(number):
    first = num2digits(number)
    second = num2digits(number, descend=False)
    return digits2num(first), digits2num(second)

def spline(y):
    a = y[0]
    b = 0
    c = 3*(y[1]-y[0])
    d = 2*(y[0]-y[1])
    return {'a':a, 'b': b, 'c': c, 'd': d}

def cubic_poly(x1, x2, spline):
    x = [x1 + (x2-x1)*i/1000 for i in range(1001)]
    diff = x2-x1
    a = spline['a']
    b = spline['b']
    c = spline['c']
    d = spline['d']
    return x, [a + b*((t-x1)/diff) + c*(((t-x1)/diff)**2) + d*(((t-x1)/diff)**3)  for t in x]

def generate_sequence():
    ##This function generate the Kaprekar sequence for each 4-digit positive integer.
    numbers = range(1000, 9999+1)
    kaprekar_dict = {1000: {'sequence': [1000]}}

    for num in numbers:
        if len(set(str(num))) == 1:
            pass
        else:
            first, second = make_pair(num)
            if (first not in kaprekar_dict.keys()):
                kaprekar_dict[first]={'sequence': [first]}
            initial = first
            while (7641 not in kaprekar_dict[initial]['sequence']):
                result = first - second
                kaprekar_dict[initial]['sequence'].append(make_pair(result)[0])
                first, second = make_pair(result)
            nsteps = len(kaprekar_dict[initial]['sequence'])-1
            kaprekar_dict[initial]['length'] = nsteps
            
    return kaprekar_dict

def plot(filter_type = False, filter_value = False, length_plot=False):
    keys = kaprekar_dict.keys()
    fig, ax = plt.subplots()
    ax2 = ax.twinx()
    if (filter_type != False):
        if (filter_type == 'length'):
            if not (1 <= filter_value <= 7):
                return None
        elif (filter_type == 'number'):
            sorted_digits = make_pair(filter_value)[0]
            if not (1000 <= sorted_digits <= 9999):
                return None
        else:
            return None

    plotted_numbers = []
    count = 0
    for key in keys:
        if (filter_type == 'length'):
            n=len(kaprekar_dict[key]['sequence'])
            if (n-1) != filter_value:
                continue
        if (filter_type == 'number'):
            n=len(kaprekar_dict[key]['sequence'])
            if key != sorted_digits:
                continue
        
        ax.plot(kaprekar_dict[key]['sequence'], '-', color=(0,0,0,0.7), lw=0.25)
        ax.plot(n-1, 7641, 'o', color = (1,0,0,0.5))
        if length_plot:
            x, poly = cubic_poly(kaprekar_dict[key]['length'], 10, spline([7641,key]))
            ax2.plot(x, poly, '-', color=(0,0,1,0.7), lw=0.25)
        plotted_numbers.append(key)
    
    if (filter_type == 'length'):
        ax.set_title("n={}".format(filter_value), fontproperties = sofia_regular)
        ax.text(filter_value, 7800, '7641 (6174)', fontproperties = sofia_regular, ha = 'center', va = 'center')

    if (filter_type == 'number'):
        ax.text(n-1, 7800, '7641 (6174)', fontproperties = sofia_regular, ha = 'center', va = 'center')

    MEAN = round(statistics.mean(plotted_numbers),2)    
    MIN, MAX = min(plotted_numbers), max(plotted_numbers)
    ax.set_yticks([MIN, MEAN, MAX])
    ax2.set_yticks([MIN, MAX])
    ax.set_yticklabels([str(MIN), str(MEAN)+"\n(Mean)", str(MAX)], fontproperties = sofia_regular)
    ax2.set_yticklabels([str(MIN), str(MAX)], fontproperties = sofia_regular)

    plt.tight_layout()

    plt.show()

kaprekar_dict = generate_sequence()
plot(length_plot=True, filter_type='length', filter_value=2)
