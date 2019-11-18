#!python
# -*- coding: utf-8 -*-
__version__ = "$Revision: 1.9 $"
# $Source: /home/mechanoid/documents/_work/texts-process-py/src/07-clasterizer-text/RCS/main.py,v $
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#
#       OS : GNU/Linux 4.8.13-1-ARCH 
# COMPILER : Python 3.6.0
#
#   AUTHOR : Evgeny S. Borisov
# 
#    http://www.mechanoid.kiev.ua
#  e-mail : nn@mechanoid.kiev.ua
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

import sys 

import numpy as np

import re
from Stemmer import Stemmer


import matplotlib.pyplot as plt
from matplotlib import cm

import sqlite3 as sq
import datetime
import hashlib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# очистка текста с помощью regexp
def text_cleaner(text):
    text = text.lower() # приведение в lowercase,
    
    text = re.sub( r'https?://[\S]+', ' url ', text) # замена интернет ссылок
    text = re.sub( r'[\w\./]+\.[a-z]+', ' url ', text) 
 
    text = re.sub( r'\d+[-/\.]\d+[-/\.]\d+', ' date ', text) # замена даты и времени
    text = re.sub( r'\d+ ?гг?', ' date ', text) 
    text = re.sub( r'\d+:\d+(:\d+)?', ' time ', text) 

    # text = re.sub( r'@\w+', ' tname ', text ) # замена имён twiter
    # text = re.sub( r'#\w+', ' htag ', text ) # замена хештегов

    text = re.sub( r'<[^>]*>', ' ', text) # удаление html тагов
    text = re.sub( r'[\W]+', ' ', text ) # удаление лишних символов

    stemmer = Stemmer('russian')
    text = ' '.join( stemmer.stemWords( text.split() ) ) 

    stw = ['в', 'по', 'на', 'из', 'и', 'или', 'не', 'но', 'за', 'над', 'под', 'то',
           'a', 'at', 'on', 'of', 'and', 'or', 'in', 'for', 'at' ]
    remove = r'\b('+'|'.join(stw)+')\b'
    text = re.sub(remove,' ', text)
    
    text = re.sub( r'\b\w\b', ' ', text ) # удаление отдельно стоящих букв

    text = re.sub( r'\b\d+\b', ' digit ', text ) # замена цифр 

    return  text

# - - - - - - - - - - - - - - - - - - - - 
def load_data():
    dbname = 'data/rss-all.sqlite'
    data = { 'text':[],'tag':[] }
    conn = sq.connect(dbname)
    try:
        c = conn.cursor()
        for row in c.execute('SELECT * FROM data'):
            data['text'] += [row[1]]
            data['tag'] += [row[2]]
    finally:
        conn.close()
    return data


# - - - - - - - - - - - - - - - - - - - - 
def save2db(data):
    dbname = 'result/result.sqlite'
    conn = sq.connect(dbname)
    try:
        c = conn.cursor()
        c.execute("CREATE TABLE data(id TEXT PRIMARY KEY, txt TEXT, tag TEXT)")

        for n in range(0,len(data['text'])):
            t = data['text'][n] + str(data['tag'][n]) + str(datetime.datetime.now())
            rec_hash = hashlib.sha256(t.encode('utf-8')).hexdigest()
            c.execute("INSERT INTO data VALUES (?, ?, ?)",  (rec_hash, data['text'][n] , str(data['tag'][n]) ) )

        conn.commit()

    finally:
        conn.close()



# - - - - - - - - - - - - - - - - - - - - 
def main():
    print("[i] загружаем данные...")
    data = load_data()
    print("\tсчитано: ",len(data['text']))

    print("[i] очистка данных...")
    D = [ text_cleaner(t) for t in data['text'] ]

    n_clusters=14

    print("[i] обучение кластеризатора...")
    text_clstz = Pipeline([
                    ('tfidf', TfidfVectorizer()),
                    ( 'km', KMeans(n_clusters=n_clusters)),
                    #( 'km', KMeans(n_clusters=n_clusters, init='random', n_init=10, max_iter=300, tol=1e-04, random_state=0) )
                    ])

    text_clstz.fit(D)
    data['tag'] = text_clstz.predict(D)

    print("\tколичество кластеров:",len(set(data['tag'])))
    
    print("[i] сохраняем результат...")

    save2db(data)


# - - - - - - - - - - - - - - - - - - - - 
if __name__ == '__main__':
    sys.exit( main() )




