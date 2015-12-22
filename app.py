from flask import Flask, request, redirect, render_template
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

db.create_all()
db.session.commit()

@app.route('/')
def show_frontpage():
    return render_template('home.html')

@app.route('/all/')
def show_all():
    OPs = get_OPs_all()
    list = []
    for OP in OPs:
        replies = get_last_replies(OP.id)
        list.append(OP)
        list += replies[::-1]

    return render_template('show_all.html', entries=list, board='all')

@app.route('/<board>/')
def show_board(board):
    if board_inexistent(board):
        return redirect('/')
    OPs = get_OPs(board)
    list = []
    for OP in OPs:
        replies = get_last_replies(OP.id)
        list.append(OP)
        list += replies[::-1]

    sidebar = get_sidebar(board)

    return render_template('show_board.html', entries=list, board=board, sidebar=sidebar, id=0)

@app.route('/<board>/catalog')
def show_catalog(board):
    OPs = get_OPs_catalog(board)
    sidebar = get_sidebar(board)

    return render_template('show_catalog.html', entries=OPs, board=board, sidebar=sidebar)

@app.route('/<board>/<id>/')
def show_thread(board, id):
    OP      = get_thread_OP(id)
    replies = get_replies(id)
    sidebar = get_sidebar(board)

    return render_template('show_thread.html', entries=OP+replies, board=board, id=id, sidebar=sidebar)

@app.route('/add', methods=['POST'])
def new_thread():
    board = request.form['board']
    if no_image():
        return redirect('/' + board + '/')

    newPost = new_post(board)
    newPost.last_bump = datetime.now()
    db.session.add(newPost)
    db.session.commit()
    return redirect('/' + board + '/')

@app.route('/add_reply', methods=['POST'])
def add_reply():
    board  = request.form['board']
    thread = request.form['op_id']
    if no_content_or_image():
        return redirect('/' + board + '/')

    newPost = new_post(board, thread)
    db.session.add(newPost)
    if 'sage' not in request.form['email'] and reply_count(thread) < BUMP_LIMIT:
        bump_thread(thread)
    db.session.commit()
    return redirect('/' + board + '/' + thread)

@app.route('/del')
def delete():
    post_id = request.args.get('id')
    delete_post(post_id)
    board   = request.args.get('board')
    thread  = request.args.get('thread')
    return redirect('/' + board + '/' + thread)

if __name__ == '__main__':
    print(' * Running on http://localhost:5000/ (Press Ctrl-C to quit)')
    print(' * Database is', SQLALCHEMY_DATABASE_URI)
    app.run()
