import os

DEBUG = True
SECRET_KEY = 'hunter2'
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_TRACK_MODIFICATIONS = False

BUMP_LIMIT         = 100
BOARDS             = ['create','learn','media','meta']
UPLOAD_FOLDER      = 'static/images/'
THUMBS_FOLDER      = 'static/thumbs/'
ALLOWED_EXTENSIONS =  set(['png','jpg','jpeg','gif'])
