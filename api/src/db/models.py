from base64 import b64encode, urlsafe_b64encode
from datetime import datetime
from secrets import token_bytes

import bcrypt
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Identity,
    Integer,
    String,
    Table,
    Text,
)
from sqlalchemy.orm import Session, declarative_base, relationship

from src.db.mixins import AppConfigurationMixin, ValidationMixin
from src.db.utils import delete_file
from src.db.validation import (
    COLOR_REGEXP,
    EMAIL_REGEXP,
    LINK_REGEXP,
    PASSWORD_REGEXP,
    TAG_REGEXP,
    USERNAME_REGEXP,
)


Base = declarative_base()


class User(Base, ValidationMixin, AppConfigurationMixin):
    __tablename__ = 'users'

    validators = {
        'username': lambda val: USERNAME_REGEXP.fullmatch(val) is not None,
        'email': lambda val: EMAIL_REGEXP.fullmatch(val) is not None,
        'password': lambda val: PASSWORD_REGEXP.fullmatch(val) is not None,
        'profile_color': lambda val: COLOR_REGEXP.fullmatch(val) is not None,
        'profile_picture_filename': lambda _: True,  # User can't control this
    }

    def __init__(
        self, username: str, email: str, password: str, is_superuser: bool = False
    ):
        self.validate_fields(username=username, email=email, password=password)
        self.username = username
        self.email = email
        self.is_superuser = is_superuser
        self.password = password

    id: int = Column(Integer, primary_key=True)
    is_superuser: bool = Column(Boolean, nullable=False, default=False)
    username: str = Column(String(80), unique=True, nullable=False)
    email: str = Column(String(120), unique=True, nullable=False)
    password_hash: str = Column(String(100), nullable=False)
    profile_color: str = Column(String(7), nullable=False, default='#ffffff')
    jwt_proof: str = Column(
        String(12), nullable=False, default=lambda: b64encode(token_bytes(9)).decode()
    )
    _profile_picture_filename: str | None = Column(
        'profile_picture_filename', String(40), nullable=True, default=None
    )
    notes: list['Note'] = relationship(
        'Note',
        backref='user',
        lazy='selectin',
        order_by='desc(Note.creation_date)',
        cascade="save-update, merge, delete, delete-orphan",
    )

    @property
    def password(self):
        raise AttributeError('password: write-only property')

    @password.setter
    def password(self, value):
        salt: bytes = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(value.encode(), salt).decode()

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())

    @property
    def profile_picture_filename(self) -> str | None:
        return self._profile_picture_filename

    @profile_picture_filename.setter
    def profile_picture_filename(self, value: str | None):
        if self._profile_picture_filename is not None:
            delete_file(self.config.file_upload, self._profile_picture_filename)
        self._profile_picture_filename = value

    def reset_profile_picture(self):
        self.profile_picture_filename = None

    def regenerate_jwt_proof(self):
        self.jwt_proof = b64encode(token_bytes(9)).decode()


note_tag_association_table = Table(
    'note_tag_association',
    Base.metadata,
    Column('note_id', ForeignKey('notes.id'), primary_key=True),
    Column('tag_id', ForeignKey('tags.id'), primary_key=True),
)


class Note(Base, ValidationMixin):
    __tablename__ = 'notes'

    validators = {
        'title': lambda val: 1 <= len(val) <= 65,
        'content': lambda val: len(val) >= 1,
        'link': lambda val: LINK_REGEXP.fullmatch(val) is not None,
        'is_private': lambda val: type(val) == bool,
        'tags': lambda tags: all(
            TAG_REGEXP.fullmatch(tag.content) is not None for tag in tags
        ),
    }

    def __init__(
        self,
        title: str,
        content: str,
        tags: list['Tag'],
        link: str,
        is_private: bool = False,
    ):
        self.validate_fields(
            title=title, link=link, content=content, is_private=is_private, tags=tags
        )
        self.title = title
        self.content = content
        self.link = link
        self.is_private = is_private
        self.tags = tags

    id: str = Column(
        String(12),
        primary_key=True,
        default=lambda: urlsafe_b64encode(token_bytes(9)).decode(),
    )
    row_id: int = Column(Integer, Identity(start=0, minvalue=0, increment=1))
    title: str = Column(String(65), nullable=False)
    content: str = Column(Text(), nullable=False)
    link: str = Column(Text(), nullable=False)
    is_private: bool = Column(Boolean(), nullable=False, default=True)
    creation_date: datetime = Column(DateTime, nullable=False, default=datetime.now)

    user: User
    _owner_id: int = Column(
        Integer,
        ForeignKey(User.id),
        name='owner_id',
        nullable=False,
    )

    tags: list['Tag'] = relationship(
        'Tag', secondary=note_tag_association_table, backref='notes', lazy="selectin"
    )


class Tag(Base, ValidationMixin):
    __tablename__ = 'tags'

    def __init__(self, content: str):
        content = content.lower()
        self.content = content

    id: int = Column(Integer, primary_key=True)
    content: str = Column(String(30), nullable=False)

    notes: list[Note]

    @classmethod
    def get_tag(cls, session: Session, content: str):
        tag: Tag | None = (
            session.query(Tag).filter(Tag.content == content.lower()).one_or_none()
        )
        if tag is not None:
            return tag
        return cls(content)
