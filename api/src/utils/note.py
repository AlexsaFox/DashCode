from typing import cast

from pydantic import NoneIsAllowedError
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
    return note


def edit_note(
    session: Session,
    title: str | None,
    content: str | None,
    link: str | None,
    is_private: bool | None,
    user: User,
    note_id: str,
) -> Note:
    note: Note | None = session.query(Note).filter(Note.id == note_id).first()

    if note is None:
        raise NoteNotFoundError
    if note.user != user:
        raise NoteOwnerError

    note.update_fields(
        session=session, title=title, content=content, link=link, is_private=is_private
    )
    return cast(Note, note)


def get_note(session: Session, id: str, user: User) -> Note:
    note = session.query(Note).filter(Note.id == id).first()

    if note is None:
        raise NoteNotFoundError
    if note.user != user:
        raise NoteOwnerError
    return cast(Note, note)


def remove_note(session: Session, id: str, user: User) -> Note:
    note = session.query(Note).filter(Note.id == id).first()
    if note is None:
        raise NoteNotFoundError
    if note.user != user:
        raise NoteOwnerError
    session.add(note)
    session.delete(note)
    session.commit()
    return cast(Note, note)


class NoteNotFoundError(ExpectedError):
    def __init__(self, msg: str = 'Unable to find a note with provided id'):
        super().__init__(msg)


class NoteOwnerError(ExpectedError):
    def __init__(
        self, msg: str = "You haven't got permission to see note with provided id"
    ):
        super().__init__(msg)
