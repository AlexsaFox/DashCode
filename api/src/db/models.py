from base64 import urlsafe_b64encode
from datetime import datetime
from secrets import token_bytes
from typing import TYPE_CHECKING

import bcrypt
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
)
from sqlalchemy.orm import declarative_base, relationship

from src.db.validation import (
    EMAIL_REGEXP,
    PASSWORD_REGEXP,
    USERNAME_REGEXP,
    ValidationError,
)


if TYPE_CHECKING:
    hybrid_property = property
else:
    from sqlalchemy.ext.hybrid import hybrid_property


Base = declarative_base()


class User(Base):
    # fmt: off
    if TYPE_CHECKING:
        def __init__(self, username: str, email: str, is_superuser: bool = ...): ...
    # fmt: on

    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True)
    is_superuser: bool = Column(Boolean, nullable=False, default=False)
    _username: str = Column('username', String(80), unique=True, nullable=False)
    _email: str = Column('email', String(120), unique=True, nullable=False)
    password_hash: str = Column(String(100), nullable=False)
    profile_color: str = Column(String(7), nullable=False, default='#ffffff')
    profile_picture_filename: str = Column(
        String(40), nullable=False, default='default.webp'
    )
    notes: list['Note'] = relationship('Note', backref='user', lazy='select')

    @hybrid_property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        if not EMAIL_REGEXP.fullmatch(value):
            raise ValidationError('email', value)
        self._email = value

    @hybrid_property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, value: str):
        if not USERNAME_REGEXP.fullmatch(value):
            raise ValidationError('username', value)
        self._username = value

    @hybrid_property
    def password(self) -> str:
        raise AttributeError("can't access password")

    @password.setter
    def password(self, value: str):
        if not PASSWORD_REGEXP.fullmatch(value):
            raise ValidationError('password', value)
        salt: bytes = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(value.encode(), salt).decode()


note_tag_association_table = Table(
    'note_tag_association',
    Base.metadata,
    Column('note_id', ForeignKey('notes.id'), primary_key=True),
    Column('tag_id', ForeignKey('tags.id'), primary_key=True),
)


class Note(Base):
    __tablename__ = 'notes'

    id: str = Column(
        String(12),
        primary_key=True,
        default=lambda: urlsafe_b64encode(token_bytes(9)).decode(),
    )
    title: str = Column(String(65), nullable=False)
    content: str = Column(Text(), nullable=False)
    link: str = Column(Text(), nullable=False)
    is_private: bool = Column(Boolean(), nullable=False, default=True)
    creation_date: datetime = Column(DateTime, nullable=False, default=datetime.now)

    user: User
    _owner_id: int = Column(
        Integer, ForeignKey(User.id), name='owner_id', nullable=False
    )

    tags: list['Tag'] = relationship(
        'Tag', secondary=note_tag_association_table, backref='notes'
    )


class Tag(Base):
    __tablename__ = 'tags'

    id: int = Column(Integer, primary_key=True)
    content: str = Column(String(30), nullable=False)

    notes: list[Note]
