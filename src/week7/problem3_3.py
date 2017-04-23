'''
Created on Mar 7, 2017

@author: Luca Fontanili
'''
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegressionCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

def svm_linear(dataset, out):
    print('svm_linear')
    X = dataset[['x', 'y']]
    y = dataset.label
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=0)
    tuned_parameters = [{'kernel': ['linear'], 'C': [0.1, 0.5, 1, 5, 10, 50, 100]}]
    
    clf = GridSearchCV(SVC(), tuned_parameters, cv=5)
    clf.fit(X_train, y_train)
    best_param = clf.best_params_
    print('best param: ' + str(best_param))
#     means = clf.cv_results_['mean_test_score']
#     stds = clf.cv_results_['std_test_score']
#     for mean, std, params in zip(means, stds, clf.cv_results_['params']):
#         print("%0.3f (+/-%0.03f) for %r"
#               % (mean, std * 2, params))
    best_score = clf.best_score_
    print('best score: ' + str(best_score))
    print('test score: ' + str(clf.score(X_test,y_test)))    
    out.write('svm_linear,' + str(best_score) + ',' + str(clf.score(X_test,y_test)) + '\n')
    
def svm_polynomial(dataset, out):
    print('svm_polynomial')
    X = dataset[['x', 'y']]
    y = dataset.label
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=0)
#     tuned_parameters = [{'kernel': ['poly'], 'C': [0.1, 1, 3], 'degree':[4, 5, 6], 'gamma':[0.1,1]}]
    tuned_parameters = [{'kernel': ['poly'], 'C': [0.1,1,3], 'degree':[4,5,6], 'gamma':[0.1,1]}]
    
    clf = GridSearchCV(SVC(), tuned_parameters, cv=5)
    clf.fit(X_train, y_train)
    best_param = clf.best_params_
    print('best param: ' + str(best_param))
    best_score = clf.best_score_
    print('best score: ' + str(best_score))
    print('test score: ' + str(clf.score(X_test,y_test)))    
    out.write('svm_polynomial,' + str(best_score) + ',' + str(clf.score(X_test,y_test)) + '\n')

def svm_rbf(dataset, out):
    print('svm_rbf')
    X = dataset[['x', 'y']]
    y = dataset.label
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=0)
#     tuned_parameters = [{'kernel': ['poly'], 'C': [0.1, 1, 3], 'degree':[4, 5, 6], 'gamma':[0.1,1]}]
    tuned_parameters = [{'kernel': ['rbf'], 'C': [0.1, 0.5, 1, 5, 10, 50, 100], 'gamma':[0.1, 0.5, 1, 3, 6, 10]}]
    
    clf = GridSearchCV(SVC(), tuned_parameters, cv=5)
    clf.fit(X_train, y_train)
    best_param = clf.best_params_
    print('best param: ' + str(best_param))
    best_score = clf.best_score_
    print('best score: ' + str(best_score))
    print('test score: ' + str(clf.score(X_test,y_test)))    
    out.write('svm_rbf,' + str(best_score) + ',' + str(clf.score(X_test,y_test)) + '\n')
    
def logistic(dataset, out):
    print('logistic')
    X = dataset[['x', 'y']]
    y = dataset.label
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=0)
    logreg = LogisticRegressionCV(Cs =[0.1, 0.5, 1, 5, 10, 50, 100] , cv=5)
    logreg.fit(X_train, y_train)    
    print('best score: ' + str(logreg.scores_[1].max()))
    print('test score: ' + str(logreg.score(X_test, y_test)))
    out.write('logistic,' + str(logreg.scores_[1].max()) + ',' + str(logreg.score(X_test, y_test)) + '\n')

def knn(dataset, out):
    print('knn')
    X = dataset[['x', 'y']]
    y = dataset.label
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=0)
    best_score = 0
    best_negih = None
    for k in range(1,51):
        for leaf_size in range(5,65,5):
            neigh = KNeighborsClassifier(n_neighbors=k, leaf_size=leaf_size)
            neigh.fit(X_train, y_train) 
            current_test_score = cross_val_score(neigh, X_train, y_train, cv=5).mean()
            if current_test_score > best_score:
                best_score = current_test_score
                best_negih = neigh

    print('best score: ' + str(best_score))
    test_score = best_negih.score(X_test, y_test)
    print('test score: ' +  str(test_score))
    out.write('knn,' + str(best_score) + ',' + str(test_score) + '\n')

def decision_tree(dataset, out):
    print('decision_tree')
    X = dataset[['x', 'y']]
    y = dataset.label
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=0)
    best_score = 0
    best_clf = None
    for max_depth in range(1,51):
        for min_sample in range(2,11):
            clf = DecisionTreeClassifier(max_depth=max_depth, min_samples_split=min_sample)
            clf.fit(X_train, y_train)
            current_test_score = cross_val_score(clf, X_train, y_train, cv=5).mean()
            if current_test_score > best_score:
                best_score = current_test_score
                best_clf = clf

    print('best score: ' + str(best_score))
    test_score = best_clf.score(X_test, y_test)
    print('test score: ' +  str(test_score))
    out.write('decision_tree,' + str(best_score) + ',' + str(test_score) + '\n')  
    
def random_forest(dataset, out):
    print('random_forest')
    X = dataset[['x', 'y']]
    y = dataset.label
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=0)
    best_score = 0
    best_clf = None
    for max_depth in range(1,51):
        for min_sample in range(2,11):
            print('md: ', max_depth, ' ms: ', min_sample)
            clf = RandomForestClassifier(max_depth=max_depth, min_samples_split=min_sample)
            clf.fit(X_train, y_train)
            current_test_score = cross_val_score(clf, X_train, y_train, cv=5).mean()
            if current_test_score > best_score:
                best_score = current_test_score
                best_clf = clf

    print('best score: ' + str(best_score))
    test_score = best_clf.score(X_test, y_test)
    print('test score: ' +  str(test_score))
    out.write('random_forest,' + str(best_score) + ',' + str(test_score))             

def main():
    inp = open('input3.csv', 'r')
    out = open('output3.csv', 'w')
    values = []
    for line in inp:
        if 'label' in line:
            continue
        params = line.strip().split(",")
        values.append((float(params[0]),float(params[1]),int(params[2])))

    dataset = pd.DataFrame(values,columns=['x','y','label'])
#     dataset.plot(x='x', y='y', kind='scatter', c='label')
#     plt.show()
    svm_linear(dataset, out)
    svm_polynomial(dataset, out)
    svm_rbf(dataset, out)
    logistic(dataset, out)
    knn(dataset, out)
    decision_tree(dataset, out)
    random_forest(dataset, out)

#     clf = SVC()
#     clf.fit(X, y) 
#     SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape=None, degree=3, gamma='auto', kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True,tol=0.001, verbose=False)


    plt.show()

if __name__ == '__main__':
    main()