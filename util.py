from flask import request, flash, redirect, url_for
from time import time
from os.path import join
from PIL import Image

from config import *

def board_inexistent(name):
    if name not in BOARDS:
        flash('board ' + name + ' does not exist')
        return True

def upload_file():
    file = request.files['file']
    fname = ''
    if file and allowed_file(file.filename):
        # Save file as <timestamp>.<extension>
        ext = file.filename.rsplit('.', 1)[1]
        fname = str(int(time() * 1000)) + '.' + ext
        file.save(join(UPLOAD_FOLDER, fname))

        # Pass to PIL to make a thumbnail
        file = Image.open(file)
        file.thumbnail((200,200), Image.ANTIALIAS)
        file.save(join(THUMBS_FOLDER, fname))
    return fname

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def no_image():
    if not request.files['file']:
        flash('Must include an image')
        return True
    return False

def no_content_or_image():
    if not request.files['file'] and request.form['post_content'] == '':
        flash('Must include a comment or image')
        return True
    return False
