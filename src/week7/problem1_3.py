'''
Created on Mar 4, 2017

@author: Luca Fontanili
'''

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def main():
    inp = open('input1.csv', 'r')
    out = open('output1.csv', 'w')
    values = []
    for line in inp:
        params = line.strip().split(",")
        values.append((1, int(params[0]),int(params[1]),int(params[2])))

    dataset = pd.DataFrame(values,columns=['ones', 'x','y','label'])

    print(dataset)
    weights = np.zeros(3)
    run = True
    x = np.linspace(0,15)
    while run is True:
        global_error = 0
        for item in dataset.values:
            fx = activation(weights,item);
            if item[3] * fx <= 0:
                weights += item[3]*np.array([item[0],item[1],item[2]])
                global_error += 1
        print(weights)
        if global_error == 0:
            run = False
        out.write(str(int(weights[1])) + ',' + str(int(weights[2])) + ',' + str(int(weights[0])) + '\n')
        y = (weights[0] + weights[1] * x) / -weights[2]
        dataset[['x','y','label']].plot(x='x', y='y', kind='scatter', c='label')
        plt.plot(x, y)
        plt.show()
    
def activation(weights, item):
    return 1 if np.sum(weights*[item[0],item[1], item[2]]) > 0 else -1

if __name__ == '__main__':
    main()