from app import db
from .user import User


def db_add(data: db.Model):
    db.session.add(data)
    db.session.commit()

def db_save_changes():
    db.session.commit()

def db_remove(data: db.Model):
    db.session.delete(data)
    db.session.commit()