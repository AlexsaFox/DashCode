from base64 import urlsafe_b64decode
from datetime import datetime
from secrets import token_bytes

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    ForeignKey,
    String,
    Table,
    Text,
)
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True)  # type: ignore
    is_superuser: bool = Column(Boolean, nullable=False, default=False)  # type: ignore
    username: str = Column(String(80), unique=True, nullable=False)  # type: ignore
    email: str = Column(String(120), unique=True, nullable=False)  # type: ignore
    password_hash: str = Column(String(100), nullable=False)  # type: ignore
    profile_color: str = Column(String(7), nullable=False, default='#ffffff')  # type: ignore
    profile_picture_filename: str = Column(
        String(40), nullable=False, default='default.webp'
    )  # type: ignore

    notes: list['Note'] = relationship('Note', backref='user', lazy=True)


note_tag_association_table = Table(
    'note_tag_association',
    Base.metadata,
    Column('note_id', ForeignKey('notes.id'), primary_key=True),
    Column('tag_id', ForeignKey('tags.id'), primary_key=True),
)


class Note(Base):
    __tablename__ = 'notes'

    id: str = Column(
        String(12), primary_key=True, default=lambda: urlsafe_b64decode(token_bytes(12))
    )  # type: ignore
    title: str = Column(String(65), nullable=False)  # type: ignore
    content: str = Column(Text(), nullable=False)  # type: ignore
    link: str = Column(Text(), nullable=False)  # type: ignore
    is_private: bool = Column(Boolean(), nullable=False, default=True)  # type: ignore
    creation_date: datetime = Column(DateTime, nullable=False, default=datetime.now)  # type: ignore

    user: User
    _owner_id: int = Column(Integer, ForeignKey(User.id), name='owner_id', nullable=False)  # type: ignore

    tags: list['Tag'] = relationship(
        'Tag', secondary=note_tag_association_table, backref='notes'
    )  # type: ignore


class Tag(Base):
    __tablename__ = 'tags'

    id: int = Column(Integer, primary_key=True)  # type: ignore
    content: str = Column(String(30), nullable=False)  # type: ignore

    notes: list[Note]
