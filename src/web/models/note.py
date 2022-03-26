from app import db
from uuid import uuid4
from .user import User


class Note(db.Model):

    __tablename__ = 'notes'

    def _get_note_uuid() -> str:
        return str(uuid4())
         
    id = db.Column(db.String(36), name='id',primary_key=True,unique=True,nullable=False,
                   default=_get_note_uuid)
    title = db.Column(db.String(65),nullable=False)
    context = db.Column(db.Text(),nullable=False)
    link = db.Column(db.Text(),nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    is_private = db.Column(db.Boolean(),nullable=False,default=True)
    


        