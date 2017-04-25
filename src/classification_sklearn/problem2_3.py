'''
Created on Mar 5, 2017

@author: Luca Fontanili
'''
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

def main(args):
    n_iter = 100
    if len(args) != 3:
        raise ValueError('Bad argument list')
    inp = open(args[1], 'r')
    learning_rates = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 0.53]
    out = open(args[2], 'w')
    values = []
    for line in inp:
        params = line.strip().split(",")
        values.append((1, float(params[0]),float(params[1]),float(params[2])))

    dataset = pd.DataFrame(values,columns=['ones', 'age','weight','height'])
    for feature in ['age', 'weight']:
        dataset[feature] = (dataset[feature] - dataset[feature].mean())/dataset[feature].std()
    
    X = dataset[['ones', 'age', 'weight']]
    y = dataset[['height']]
    
    for alpha in learning_rates:
        beta = np.zeros(3)
#         print('new alpha: ',alpha)
        for i in range(n_iter):
            old_beta = np.array(beta)
            count = 0
            for feature in ['ones', 'age', 'weight']:
                beta[count] = old_beta[count] - alpha/len(y) * np.sum(((X.dot(old_beta) - y.transpose())*(X[feature].transpose())).transpose())
                count += 1
#             print(beta)
#         print(compute_cost(X, beta, y))
        out.write(str(alpha) + ',' + str(n_iter) + ',' + str(beta[0]) + ',' + str(beta[1]) + ',' + str(beta[2]) + '\n')

    threedee = plt.figure().gca(projection='3d')
    threedee.scatter(dataset['age'], dataset['weight'], dataset['height'])
    threedee.set_xlabel('Age (years)')
    threedee.set_ylabel('Weight (kilos)')
    threedee.set_zlabel('Height (meters)')
    
#     threedee.plot_surface(xx,yy,z1, color='blue')
    plt.show()
    
def compute_cost(X, beta, y):
    squared_error = np.sum(((X.dot(beta)-y.transpose())**2).transpose())
    J = squared_error/(2*len(y))
    return J

if __name__ == '__main__':
    main(sys.argv)