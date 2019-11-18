#!python
# -*- coding: utf-8 -*-
__version__ = "$Revision: 1.4 $"
# $Source: /home/mechanoid/www/mechanoid.home.lan/htdocs/content/ml-text-proc.html/src/db-editor/RCS/textsdb.py,v $
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#
#       OS : GNU/Linux 4.7.6-1-ARCH 
# COMPILER : Python 3.5.2
#
#   AUTHOR : Evgeny S. Borisov
# 
#    http://www.mechanoid.kiev.ua
#  e-mail : nn@mechanoid.kiev.ua
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
import numpy as np
import sqlite3 

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
class TextsDB:

    def __init__(self,dbname=''):
        self.dbname = dbname
        self.conn = None
        self.cursor = None
        self.open(dbname)

    def open(self,dbname):
        if dbname:
            self.dbname = dbname
            self.close()
            self.conn = sqlite3.connect(self.dbname)
            if self.conn:
                self.cursor = self.conn.cursor()
        else:
            print('[E] bad DB name')

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None


    def __del__(self):
        self.close()


    def get(self,offset=0,size=1,filt=''):
        if not self.cursor:
            print('[E] get: DB is not opened')
            return None

        data = {'text':[],'tag':[],'id':[]}

        if filt != '' and filt != '-' :
            rows = self.cursor.execute('SELECT * FROM data WHERE tag = ? LIMIT ? OFFSET ? ',(filt,size,offset))
        else:
            rows = self.cursor.execute('SELECT * FROM data LIMIT ? OFFSET ? ', (size,offset))

        for r in rows:
            data['id'] += [r[0]]
            data['text'] += [r[1]]
            data['tag'] += [r[2]]
    
        return data

    def tags(self):
        if not self.cursor:
            print('[E] tags: DB is not opened')
            return None

        tags={}
        rows = self.cursor.execute('SELECT tag, COUNT(tag) AS cnt FROM data GROUP BY tag')
        for r in rows:
            tags[ r[0] ] = r[1]

        return tags


    def len(self,filt=''):
        if not self.cursor:
            print('[E] len: DB is not opened')
            return None

        res = 0
        if filt != '' and filt != '-' :
            self.cursor.execute('SELECT COUNT(id) FROM data WHERE tag = ?',(filt,))
        else:
            self.cursor.execute('SELECT COUNT(id) FROM data')

        res = self.cursor.fetchone()[0]

        return res


    def delete(self,args):
        if not self.cursor:
            print('[E] delete: DB is not opened')
            return

        if args['id'] != '':
            self.cursor.execute('DELETE FROM data WHERE id = ? ', ( args['id'], ) )
            self.conn.commit()
        else:
            print("[E] delete: bad args")

    def update_tag(self,args):
        if not self.cursor:
            print('[E] update_tag: DB is not opened')
            return

        if args['id'] != '' and args['tag'] != '':
            self.cursor.execute('UPDATE data SET tag = ? WHERE id = ? ',( args['tag'], args['id'] ) )
            self.conn.commit()
        else:
            print("[E] update_tag: bad args")

    def update_text(self,args):
        if not self.cursor:
            print('[E] update_tag: DB is not opened')
            return
 
        if args['id'] != '' and args['text'] != '':
            self.cursor.execute('UPDATE data SET txt = ? WHERE id = ? ',( args['text'], args['id'] ) )
            self.conn.commit()
        else:
            print("[E] update_text: bad args")





# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
if __name__ == '__main__':
    pass

