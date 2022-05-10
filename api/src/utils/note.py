from typing import cast

from sqlalchemy.orm.session import Session

from src.db.models import Note, User
from src.types import ExpectedError


def create_note(
    session: Session, title: str, content: str, link: str, is_private: bool, user: User
) -> Note:
    note = Note(
        title=title,
        content=content,
        link=link,
        is_private=is_private,
    )
    session.add(user)
    user.notes.append(note)
    session.add(note)
    session.commit()
    session.refresh(note)
    session.refresh(user)
    return note


def get_note(session: Session, id: str, user: User) -> Note:
    note = session.query(Note).filter(Note.id == id).first()

    if note is None:
        raise NoteNotFoundError
    if note.user != user:
        raise NoteOwnerError
    return cast(Note, note)


class NoteNotFoundError(ExpectedError):
    def __init__(self, msg: str = 'Unable to find a note with provided id'):
        super().__init__(msg)


class NoteOwnerError(ExpectedError):
    def __init__(
        self, msg: str = "You haven't got permission to see note with provided id"
    ):
        super().__init__(msg)
