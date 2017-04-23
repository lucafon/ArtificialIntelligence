'''
Created on Apr 1, 2017

@author: Luca Fontanili
'''
from os import listdir
from os.path import isfile, join
import re
import numpy as np
import pandas as pd
from sklearn.linear_model import SGDClassifier

vector_count = 0
def create_dataset(count, path, f, polarity):
    onlyfiles = [n_f for n_f in listdir(path) if isfile(join(path, n_f))]
    for current_file in onlyfiles:
        current = open(join(path,current_file),'r')
        text = current.read().rstrip()
        text = text.replace('\n', ' ').replace('<br />', ' ').lower()
        f.write(str(count) + ',' + re.sub('[^0-9a-zA-Z ]+', '', text) + ',' + polarity + '\n')
        count += 1
    return count

def write_file():

    neg_path = 'aclImdb/train/neg'
    pos_path = 'aclImdb/train/pos'
    f = open('imdb_tr.csv', 'w')
    f.write('row_number,text,polarity\n')
          
    count = create_dataset(0, neg_path, f, '0')
    create_dataset(count, pos_path, f, '1')
    
    
def create_vector(text, words_list, words):
    global vector_count
    print(vector_count)
    vector_count += 1
    vec = np.zeros(len(words), dtype=np.int)
#     print(n.searchsorted(a, v, side, sorter))
#     vec[[i for i,n in enumerate(words_list) if n in set(text.split(' '))]] = 1
    for word in set(text.split(' ')):
        if word in words:
            vec[words_list.index(word)] = 1
    return vec.tolist()

def main():
    
    print('creating training file')
    write_file()
    print('training file created')
    stopwords = set()
    for s in open('stopwords.en.txt').read().rstrip().split('\n'):
        stopwords.add(s)
    print('creating vocabulary')
    words = set()
    dataset = pd.read_csv('imdb_tr.csv', sep=',')    
    [words.add(word) for row in dataset['text'] for word in row.split()]
    words = words.difference(stopwords)
    print('vocabulary created, size: ', str(len(words)))
    words_list = list(words)
    print('creating feature vector, ', str(len(dataset.text)))
    pos_index = range(100)
    neg_index = range(24000,24100)
    X = []
    [X.append(create_vector(text, words_list, words)) for text in dataset.iloc[pos_index].text]
    [X.append(create_vector(text, words_list, words)) for text in dataset.iloc[neg_index].text]
    print('feature vector created, size: ', str(len(X)))
#     [X.append(create_vector(position, words)) for position in dataset['text']]
    print('creating polarity vector')
    y = []
    [y.append(polarity) for polarity in dataset.iloc[pos_index].polarity]
    [y.append(polarity) for polarity in dataset.iloc[neg_index].polarity] 
    print('polarity vector created, size: ', str(len(X)))
    print('training classifier')
    clf = SGDClassifier(loss="hinge", penalty="l1")
    clf.fit(X, y)
    print('classifier trained')
    t_index = 150
    ilocT = create_vector(dataset.iloc[t_index].text, words_list, words)
    print('predicting')
    print(dataset.iloc[t_index].text)
    print(clf.predict([ilocT]))
          
if __name__ == '__main__':
    main()
