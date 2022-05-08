from base64 import urlsafe_b64encode
from datetime import datetime
from secrets import token_bytes
from typing import Any, Callable, Mapping

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
from sqlalchemy.orm import Session, declarative_base, relationship

from src.db.validation import (
    COLOR_REGEXP,
    EMAIL_REGEXP,
    PASSWORD_REGEXP,
    USERNAME_REGEXP,
    ModelFieldValidationError,
)


Base = declarative_base()


class ValidatedModel:
    validators: Mapping[str, Callable[[Any], bool]]

    def validate_fields(self, **kwargs: Any):
        kwargs = {f: v for f, v in kwargs.items() if v is not None}

        error_fields = []
        for field, value in kwargs.items():
            validate = self.validators.get(field)
            if validate is None:
                raise ValueError(f'Unknown field: {field}')

            if not validate(value):
                error_fields.append(field)

        if error_fields:
            raise ModelFieldValidationError(self, error_fields)

    def update_fields(self, session: Session, **kwargs: Any):
        kwargs = {f: v for f, v in kwargs.items() if v is not None}
        self.validate_fields(**kwargs)

        # Fields are already validated, so it's guaranteed that
        # no impostors will be among them
        for field, value in kwargs.items():
            setattr(self, field, value)

        session.add(self)
        session.commit()
        session.refresh(self)


class User(Base, ValidatedModel):
    __tablename__ = 'users'

    validators = {
        'username': lambda val: USERNAME_REGEXP.fullmatch(val) is not None,
        'email': lambda val: EMAIL_REGEXP.fullmatch(val) is not None,
        'password': lambda val: PASSWORD_REGEXP.fullmatch(val) is not None,
        'profile_color': lambda val: COLOR_REGEXP.fullmatch(val) is not None,
    }

    def __init__(
        self, username: str, email: str, password: str, is_superuser: bool = False
    ):
        self.validate_fields(username=username, email=email, password=password)
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
