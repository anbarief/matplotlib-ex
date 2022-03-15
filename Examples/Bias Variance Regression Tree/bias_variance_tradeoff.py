#Author: Arief Anbiya (2022)
#E-mail: anbarief@live.com
#Plotting the Bias-Variance trade off of a Regression Tree model to predict the data resembling x^2

import math
import random
import statistics

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from sklearn.tree import DecisionTreeRegressor as DTR


def combine(dict_input, neglected_key):
    result_x, result_y = [], []
    for i in dict_input.keys():
        if i != neglected_key:
            result_x.extend(dict_input[i]['x'])
            result_y.extend(dict_input[i]['y'])
    return result_x, result_y

def rmse(y1, y2):
    n = len(y1)
    return math.sqrt(statistics.mean([(y1[i]-y2[i])**2 for i in range(n)]))

Nfold = 20
Ndata = 2000
samples_split = range(2, 40)
df = [(40-i) + 1 for i in samples_split]
n = int(Ndata/Nfold)
X = [10*random.random() for i in range(Ndata)]
Y = [i**2 + random.gauss(0,1)  for i in X]

validation_dict = {1: {'x': X[0:n], 'y': Y[0:n] }}
start_index = n
for i in range(2, Nfold+1):
    end = start_index + n
    validation_dict[i] = {'x': X[start_index:end], 'y': Y[start_index:end]}
    start_index = end

error = {j: {i: {'train': 0, 'test': 0} for i in range(1, Nfold+1)} for j in df}
mean = {'train': [], 'test': []}
for j in df:
    model = DTR(min_samples_split=41-j)
    train_sum = 0; test_sum = 0
    for i in range(1, Nfold+1):
        Xtest, Ytest = validation_dict[i]['x'], validation_dict[i]['y'] 
        Xtrain, Ytrain = combine(validation_dict, i)
        model.fit([[k] for k in Xtrain], [[k] for k in Ytrain])
        train_result = model.predict([[k] for k in Xtrain])
        test_result = model.predict([[k] for k in Xtest])
        error[j][i]['train'] = rmse(train_result, Ytrain)
        train_sum += error[j][i]['train'] 
        error[j][i]['test'] = rmse(test_result, Ytest)
        test_sum += error[j][i]['test']
    mean['train'].append(train_sum/Nfold)
    mean['test'].append(test_sum/Nfold)

fig, ax = plt.subplots()
    
for i in range(1, Nfold+1):
    train_error = [error[j][i]['train'] for j in df]
    test_error = [error[j][i]['test'] for j in df]
    light_blue = ax.plot(df, train_error, '-', color = (0,0,1, 0.3))
    light_red = ax.plot(df, test_error, '-', color = (1,0,0, 0.3))

blue = ax.plot(df, mean['train'],'-', color = (0,0,1,1), lw=2)
red = ax.plot(df, mean['test'],'-', color = (1,0,0,1), lw=2)
ax.set_xlabel('Model complexity')
ax.set_ylabel(r'RMSE: $\sqrt{ \frac{1}{n} \sum (y_{i} - f(x_{i}))^{2})}$', rotation = 0, labelpad=70)

legend = ax.legend([light_blue[0], blue[0], light_red[0], red[0]], \
                   ['Training Error', 'Expected Training Error (approx.)', 'Test Error', 'Expected Test Error (approx.)'])

handles = legend.get_texts()
for i in handles:
    i.set_fontstyle('italic')
    i.set_fontsize(7)
    
plt.tight_layout()

fig.show()
