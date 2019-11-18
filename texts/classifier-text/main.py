#!python
# -*- coding: utf-8 -*-
__version__ = "$Revision: 1.9 $"
# $Source: /home/mechanoid/documents/_work/texts-process-py/src/06-classifier-text/RCS/main.py,v $
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#
#       OS : GNU/Linux  4.8.13-1-ARCH 
# COMPILER : Python 3.6.0
#
#   AUTHOR : Evgeny S. Borisov
# 
#    http://www.mechanoid.kiev.ua
#  e-mail : nn@mechanoid.kiev.ua
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


import sys

import numpy as np
import pickle
import sqlite3
import re

from Stemmer import Stemmer

#from sklearn.feature_extraction.text import CountVectorizer
#from sklearn.feature_extraction.text import HashingVectorizer
#from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score




# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# очистка текста с помощью regexp
def text_cleaner(text):
    text = text.lower() # приведение в lowercase,
    
    text = re.sub( r'https?://[\S]+', ' url ', text) # замена интернет ссылок
    text = re.sub( r'[\w\./]+\.[a-z]+', ' url ', text) 
 
    # text = re.sub( r'\d+[-/\.]\d+[-/\.]\d+', ' date ', text) # замена даты и времени
    # text = re.sub( r'\d+ ?гг?', ' date ', text) 
    # text = re.sub( r'\d+:\d+(:\d+)?', ' time ', text) 
    # text = re.sub( r'@\w+', ' tname ', text ) # замена имён twiter
    # text = re.sub( r'#\w+', ' htag ', text ) # замена хештегов

    text = re.sub( r'<[^>]*>', ' ', text) # удаление html тагов
    text = re.sub( r'[\W]+', ' ', text ) # удаление лишних символов

    stemmer = Stemmer('russian')
    text = ' '.join( stemmer.stemWords( text.split() ) ) 

    # stw = ['в', 'по', 'на', 'из', 'и', 'или', 'не', 'но', 'за', 'над', 'под', 'то',
    #        'a', 'at', 'on', 'of', 'and', 'or', 'in', 'for', 'at' ]
    # remove = r'\b('+'|'.join(stw)+')\b'
    # text = re.sub(remove,' ', text)
    #
    # text = re.sub( r'\b\w\b', ' ', text ) # удаление отдельно стоящих букв

    text = re.sub( r'\b\d+\b', ' digit ', text ) # замена цифр 

    return  text 


# - - - - - - - - - - - - - - - - - - - - - - - - -
# загрузка данных 
#

def load_data():
    dbname = 'data/rss-all.sqlite'

    data = { 'text':[],'tag':[] }

    conn = sqlite3.connect(dbname)
    try:
        c = conn.cursor()
        for row in c.execute('SELECT * FROM data'):
            data['text'] += [row[1]]
            data['tag'] += [row[2]]
    finally:
        conn.close()

    return data


# - - - - - - - - - - - - - - - - - - - - - - - - -
# разделение набора текстов (data)
# на тестовый и учебный наборы
# случайным образом в заданной пропорции (validation_split)
#
def train_test_split( data, validation_split = 0.2):
    sz = len(data['text'])
    indices = np.arange(sz)
    np.random.shuffle(indices)

    X = [ data['text'][i] for i in indices ]
    Y = [ data['tag'][i] for i in indices ]
    nb_validation_samples = int( validation_split * sz )

    return { 
        'train': { 'x': X[:-nb_validation_samples], 'y': Y[:-nb_validation_samples]  },
        'test': { 'x': X[-nb_validation_samples:], 'y': Y[-nb_validation_samples:]  }
    }





# - - - - - - - - - - - - - - - - - - - - 
def main():
    print("[i] загружаем данные...")
    data = load_data()
    print("\tсчитано: ",len(data['text']))

    #print("[i] очистка данных...")
    #data['text'] = [ text_cleaner(t) for t in data['text'] ]

    print("[i] разделение данных...")
    D = train_test_split( data )

    print("[i] обучение классификатора...")
    
    # text_clf = Pipeline([
    #                ('hashvect', HashingVectorizer() ),
    #                ('tfidf', TfidfTransformer(use_idf=False )),
    #                ('clf', SGDClassifier(loss='hinge')),
    #                ])
    #
    # text_clf = Pipeline([
    #                ('covect', CountVectorizer() ),
    #                ('tfidf', TfidfTransformer(preprocessor=text_cleaner,use_idf=False )),
    #                ('clf', SGDClassifier(loss='hinge')),
    #                ])


    text_clf = Pipeline([
                    ('tfidf', TfidfVectorizer()),
                    ('clf', SGDClassifier(loss='hinge')),
                    ])

    text_clf.fit(D['train']['x'], D['train']['y'])

    
    print("[i] тестируем...")

    predicted = text_clf.predict( D['train']['x'] )
    print("\taccuracy train: ", accuracy_score(  D['train']['y'] , predicted) )

    predicted = text_clf.predict( D['test']['x'] )
    print("\taccuracy test: ", accuracy_score(  D['test']['y'] , predicted) )




# - - - - - - - - - - - - - - - - - - - - 
if __name__ == '__main__':
    sys.exit( main() )



