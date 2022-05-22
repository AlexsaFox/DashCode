from typing import cast

from sqlalchemy import and_
from sqlalchemy.orm.session import Session

from src.db.models import Note, Tag, User
from src.types import ExpectedError


def create_note(
    session: Session,
    title: str,
    content: str,
    tags: list[str],
    link: str,
    is_private: bool,
    user: User,
) -> Note:
    note = Note(
        title=title,
        content=content,
        link=link,
        is_private=is_private,
        tags=[Tag.get_tag(session, tag_content) for tag_content in tags],
    )

    session.add(user)
    user.notes.append(note)

    session.add(note)

    session.commit()
    session.refresh(note)
    return note


def edit_note(
    session: Session,
    title: str | None,
    content: str | None,
    tags: list[str] | None,
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

    if tags is not None:
        new_tags = [Tag.get_tag(session, tag_content) for tag_content in tags]
        old_tags = note.tags.copy()
    else:
        new_tags = note.tags
        old_tags = []

    note.update_fields(
        session=session,
        title=title,
        content=content,
        link=link,
        is_private=is_private,
        tags=new_tags,
    )

    for tag in old_tags:
        if len(tag.notes) == 0:
            session.delete(tag)
    session.commit()

    return cast(Note, note)


def get_note(session: Session, id: str, user: User) -> Note:
    note = session.query(Note).filter(Note.id == id).first()

    if note is None:
        raise NoteNotFoundError
    if note.user != user:
        raise NoteOwnerError
    return cast(Note, note)


def remove_note(session: Session, id: str, user: User) -> Note:
    note: Note | None = session.query(Note).filter(Note.id == id).first()
    if note is None:
        raise NoteNotFoundError
    if note.user != user:
        raise NoteOwnerError

    session.add(note)
    session.delete(note)

    for tag in note.tags:
        if len(tag.notes) == 0:
            session.delete(tag)

    session.commit()
    return cast(Note, note)


def get_public_notes(
    session: Session, from_id: str | None, amount: int, newest_first: bool
) -> list[Note]:
    order_coef = -1 if newest_first else 1

    if from_id is None:
        first_note: Note | None = (
            session.query(Note).order_by(order_coef * Note.row_id).first()
        )
        if first_note is None:
            return []
        start_from_id = first_note.row_id
    else:
        start_from: Note | None = (
            session.query(Note)
            .where(and_(Note.is_private == False, Note.id == from_id))
            .first()
        )
        if start_from is None:
            raise NoteNotFoundError
        start_from_id = start_from.row_id + order_coef

    print(start_from_id)

    notes = (
        session.query(Note)
        .order_by(order_coef * Note.row_id)
        .where(
            and_(
                Note.is_private == False,
                order_coef * (Note.row_id - start_from_id) >= 0,
            )
        )
        .limit(amount)
        .all()
    )

    # Load all users to session
    for note in notes:
        session.refresh(note.user)

    return notes


class NoteNotFoundError(ExpectedError):
    def __init__(self, msg: str = 'Unable to find a note with provided id'):
        super().__init__(msg)


class NoteOwnerError(ExpectedError):
    def __init__(
        self, msg: str = "You haven't got permission to see note with provided id"
    ):
        super().__init__(msg)
