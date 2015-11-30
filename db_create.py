from app import db
from models import Boards, Posts

db.create_all()
db.session.commit()
