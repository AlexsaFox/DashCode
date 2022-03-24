from app import db
from .user import User, API_TOKEN_ERROR


def db_add(data: db.Model):
    """ Adds entry to database """
    db.session.add(data)
    db.session.commit()

def db_save_changes():
    """ Commits changes to database """
    db.session.commit()

def db_remove(data: db.Model):
    """ Removes entry from database """
    db.session.delete(data)
    db.session.commit()