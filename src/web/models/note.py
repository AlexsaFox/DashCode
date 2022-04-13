from app import db
from uuid import uuid4
from .user import User

def _get_note_uuid() -> str:
        return str(uuid4())

class Note(db.Model):

    __tablename__ = 'notes'

    id = db.Column(db.String(36),primary_key=True,unique=True,nullable=False,
                   default=_get_note_uuid)
    title = db.Column(db.String(65),nullable=False)
    context = db.Column(db.Text(),nullable=False)
    link = db.Column(db.Text(),nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    is_private = db.Column(db.Boolean(),nullable=False,default=True)

    
    


        