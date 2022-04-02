from app import db
from uuid import uuid4
from .user import User

def _get_note_uuid() -> str:
        return str(uuid4())

note_tag = db.Table('note_tags',
    db.Column('note_id', db.String(36), db.ForeignKey('notes.id')),
    db.Column('tag_id', db.String(36), db.ForeignKey('tags.id'))
)
class Note(db.Model):

    __tablename__ = 'notes'

    id = db.Column(db.String(36),primary_key=True,unique=True,nullable=False,
                   default=_get_note_uuid)
    title = db.Column(db.String(65),nullable=False)
    context = db.Column(db.Text(),nullable=False)
    link = db.Column(db.Text(),nullable=False)
    tags_arr = db.relationship('Tag',secondary=note_tag,backref='note')
    owner = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    is_private = db.Column(db.Boolean(),nullable=False,default=True)

class Tag(db.Model):
    
    __tablename__ = 'tags'

    id = db.Column(db.String(36),primary_key=True,unique=True,nullable=False,
                default=_get_note_uuid)
    title = db.Column(db.String(65),nullable=False)

    
    


        