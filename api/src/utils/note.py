from sqlalchemy.orm.session import Session
from src.db.models import User, Note


def create_note(
    session: Session, title: str, content: str, link: str, is_private: bool, user: User
) -> Note:
    note = Note(
        title=title,
        content=content,
        link=link,
        is_private=is_private,
    )
    user.notes.append(note)
    session.add(note)
    session.commit()
    session.refresh(note)
    session.refresh(user)
    return note
