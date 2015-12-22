from app import db

class Boards(db.Model):
    __tablename__ = 'boards'
    name        = db.Column(db.String, primary_key = True)
    long_name   = db.Column(db.String)
    description = db.Column(db.String)
    hidden      = db.Column(db.Boolean)

class Posts(db.Model):
    __tablename__ = 'posts'
    id        = db.Column(db.Integer, primary_key = True)
    op_id     = db.Column(db.Integer)
    board     = db.Column(db.String)
    name      = db.Column(db.String)
    subject   = db.Column(db.String)
    email     = db.Column(db.String)
    date      = db.Column(db.String)
    fname     = db.Column(db.String)
    text      = db.Column(db.Text)
    last_bump = db.Column(db.DateTime)
    deleted   = db.Column(db.Boolean)
