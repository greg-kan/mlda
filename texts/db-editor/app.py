#!python
# -*- coding: utf-8 -*-
__version__ = "$Revision: 1.29 $"
# $Source: /home/mechanoid/www/mechanoid.home.lan/htdocs/content/ml-text-proc.html/src/db-editor/RCS/app.py,v $
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


from flask import Flask
from flask import render_template
from flask import request

from textsdb import TextsDB 

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
DBNAME = 'data/result.sqlite'
#DBNAME = 'data/rss-all.sqlite'

# - - - - - - - - - - - - - -
def db_action(args):
    db = TextsDB(DBNAME)

    if   args['action'] == 'delete' :
        db.delete(args)
    elif args['action'] == 'tag'  :
        db.update_tag(args)
    elif args['action'] == 'text' :
        db.update_text(args)
    else:
        print("[E] uknown action:" , args['action'] )


def render_page(args):
    db = TextsDB(DBNAME)
   
    rec_numb = db.len(filt=args['filt_tag'])
    tags = db.tags()

    if rec_numb < 1 :
        return render_template('index.tpl',
                               text=[], 
                               tag=[],
                               text_id=[],
                               tags=tags,
                               filt_tag=args['filt_tag'],
                               rec_numb=0,
                               page=1,
                               size=1,
                               maxpage=1,
                               dbname=DBNAME,
                           )


    size = min(max(args['size'],1),rec_numb)
    maxpage = round( rec_numb / size )
    page = min(max(args['page'],1),maxpage)
    offset = (page-1)*size
    if offset >= rec_numb:
        offset = 0
        page = 1
    data = db.get(offset=offset,size=size,filt=args['filt_tag'])
  
    return render_template('index.tpl',
                           text=data['text'], 
                           tag=data['tag'],
                           text_id=data['id'],
                           tags=tags,
                           filt_tag=args['filt_tag'],
                           rec_numb=rec_numb,
                           page=page,
                           size=size,
                           maxpage=maxpage,
                           dbname=DBNAME,
                           )


# - - - - - - - - - - - - - -
# - - - - - - - - - - - - - -

app = Flask(__name__)


# - - - - - - - - - - - - - -
@app.route('/',methods = ["GET"])
def index():
    nav_args = {'page':1, 'size':1, 'filt_tag':'', }
    nav_args['page'] = request.args.get('page', type=int, default=1)
    nav_args['size'] = request.args.get('size', type=int, default=20)
    nav_args['filt_tag'] = request.args.get('filt_tag', type=str, default='')
    
    return render_page(nav_args)
   
# - - - - - - - - - - - - - -
@app.route('/',methods = ["POST"])
def index_post():
    act_args = {'id':'', 'action':'none', 'tag':'', 'text':'', }
    act_args['id'] = request.form.get('text_id', type=str, default="")
    act_args['action'] = request.form.get('action', type=str, default="none")
    act_args['tag'] = request.form.get('tag', type=str, default="")
    act_args['text'] = request.form.get('text', type=str, default="")
    
    if act_args['id'] != '' :
        db_action(act_args)

    nav_args = {'page':1, 'size':1, 'filt_tag':'', }
    nav_args['page'] = request.form.get('page', type=int, default=1)
    nav_args['size'] = request.form.get('size', type=int, default=20)
    nav_args['filt_tag'] = request.form.get('filt_tag', type=str, default='')

    return render_page(nav_args)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
if __name__ == '__main__':
    app.run()


