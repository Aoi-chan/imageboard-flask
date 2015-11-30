from flask import Flask, request, session, redirect, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from flask.ext.misaka import Misaka

app = Flask(__name__)
Misaka(app=app, escape    = True,
                no_images = True,
                wrap      = True,
                autolink  = True,
                no_intra_emphasis = True,
                space_headers     = True)

app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

from config import *
from util import *
from models import *

db.create_all()
db.session.commit()

@app.route('/')
def show_frontpage():
    return render_template('home.html')

@app.route('/all/')
def show_all():
    OPs = db.session.query(Posts).filter_by(op_id = '0').order_by(db.text('last_bump desc')).limit(10)
    list = []
    for OP in OPs:
        replies = db.session.query(Posts).filter_by(op_id = OP.id).order_by(db.text('id desc')).limit(5)
        list.append(OP)
        list += replies[::-1]

    return render_template('show_all.html', entries=list, board='all')

@app.route('/<board>/')
def show_board(board):
    if board_inexistent(board):
        return redirect('/')
    OPs = db.session.query(Posts).filter_by(op_id = '0', board = board).order_by(db.text('last_bump desc')).limit(10)
    list = []
    for OP in OPs:
        replies = db.session.query(Posts).filter_by(op_id = OP.id).order_by(db.text('id desc')).limit(5)
        list.append(OP)
        list += replies[::-1]

    sidebar = db.session.query(Boards).filter_by(name=board).first()

    return render_template('show_board.html', entries=list, board=board, sidebar=sidebar, id=0)

@app.route('/<board>/catalog')
def show_catalog(board):
    OPs = db.session.query(Posts).filter_by(op_id = '0', board = board).order_by(db.text('last_bump desc')).limit(100)
    sidebar = db.session.query(Boards).filter_by(name=board).first()

    return render_template('show_catalog.html', entries=OPs, board=board, sidebar=sidebar)

@app.route('/<board>/<id>/')
def show_thread(board, id):
    OP      = db.session.query(Posts).filter_by(id = id).all()
    replies = db.session.query(Posts).filter_by(op_id = id).all()
    sidebar = db.session.query(Boards).filter_by(name=board).first()

    return render_template('show_thread.html', entries=OP+replies, board=board, id=id, sidebar=sidebar)

@app.route('/add', methods=['POST'])
def new_thread():
    board = request.form['board']
    if no_image():
        return redirect('/' + board + '/')
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fname = upload_file()

    newPost = Posts(board   = board,
                    name    = request.form['name'],
                    subject = request.form['subject'],
                    email   = request.form['email'],
                    text    = request.form['post_content'],
                    date    = date,
                    fname   = fname,
                    op_id   = 0)     # Threads are normal posts with op_id set to 0

    newPost.last_bump = datetime.now()

    db.session.add(newPost)
    db.session.commit()
    return redirect('/' + board + '/')

@app.route('/add_reply', methods=['POST'])
def add_reply():
    board = request.form['board']
    op_id = request.form['op_id']
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if no_content_or_image():
        return redirect('/' + board + '/')
    fname = upload_file()

    newPost = Posts(board   = board,
                    name    = request.form['name'],
                    subject = request.form['subject'],
                    email   = request.form['email'],
                    text    = request.form['post_content'],
                    date    = date,
                    fname   = fname,
                    op_id   = op_id)

    db.session.add(newPost)

    reply_count = db.session.query(Posts).filter_by(op_id = op_id).count()
    if 'sage' not in request.form['email'] and reply_count < BUMP_LIMIT:
        OP = db.session.query(Posts).filter_by(id = op_id).first()
        OP.last_bump = datetime.now()
        db.session.add(OP)

    db.session.commit()
    return redirect('/' + board + '/' + op_id)

if __name__ == '__main__':
    print('Database is', SQLALCHEMY_DATABASE_URI)
    app.run()
