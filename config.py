# This configuration file is provided to make testing easy. Your real
# configuration should not be checked into source control. See:
# http://blog.arvidandersson.se/2013/06/10/credentials-in-git-repos

DEBUG = True
SECRET_KEY = 'secret'
SQLALCHEMY_DATABASE_URI = 'sqlite:///posts.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

BUMP_LIMIT         = 100
BOARDS             = ['create','learn','media','meta']
UPLOAD_FOLDER      = 'static/images/'
THUMBS_FOLDER      = 'static/thumbs/'
ALLOWED_EXTENSIONS =  set(['png','jpg','jpeg','gif'])
