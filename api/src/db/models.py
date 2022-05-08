from base64 import urlsafe_b64encode
from datetime import datetime
from secrets import token_bytes

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
    ModelFieldValidationError,
)


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    def __init__(
        self, username: str, email: str, password: str, is_superuser: bool = False
    ):
        User.validate_fields(username=username, email=email, password=password)
        self.username = username
        self.email = email
        self.is_superuser = is_superuser
        salt: bytes = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode(), salt).decode()

    id: int = Column(Integer, primary_key=True)
    is_superuser: bool = Column(Boolean, nullable=False, default=False)
    username: str = Column(String(80), unique=True, nullable=False)
    email: str = Column(String(120), unique=True, nullable=False)
    password_hash: str = Column(String(100), nullable=False)
    profile_color: str = Column(String(7), nullable=False, default='#ffffff')
    profile_picture_filename: str = Column(
        String(40), nullable=False, default='default.webp'
    )
    notes: list['Note'] = relationship(
        'Note', backref='user', lazy='select', cascade='all, delete'
    )

    @classmethod
    def validate_fields(
        self,
        username: str | None = None,
        email: str | None = None,
        password: str | None = None,
    ) -> None:
        error_fields = []

        if username is not None and not USERNAME_REGEXP.fullmatch(username):
            error_fields.append('username')

        if email is not None and not EMAIL_REGEXP.fullmatch(email):
            error_fields.append('email')

        if password is not None and not PASSWORD_REGEXP.fullmatch(password):
            error_fields.append('password')

        if error_fields:
            raise ModelFieldValidationError(error_fields)

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())


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
