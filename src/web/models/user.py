from __future__ import annotations

import re
import jwt
import datetime
from enum import Enum
from secrets import choice
from string import ascii_letters
from typing import TYPE_CHECKING

from app import db, bcrypt
from config import active_configuration

if TYPE_CHECKING:
    from werkzeug.datastructures import FileStorage


_COLOR_REGEXP = re.compile(r'#[a-fA-F0-9]{6}')


class API_TOKEN_ERROR(Enum):
    VALIDATION_ERROR = 0
    EXPIRED = 1
    BAD_STRUCTURE = 2
    NOT_FOUND = 3


def gen_random_string(size: int, alphabet: str) -> str:
    return ''.join([choice(alphabet) for _ in range(size)])

def _get_api_token() -> str:
    return gen_random_string(32, ascii_letters)

def _gen_filename() -> str:
    return gen_random_string(32, ascii_letters)

def _get_token_expiration_date() -> int:
    current_date = datetime.datetime.now()
    expiration_date = current_date + active_configuration.API_TOKEN_LIFETIME
    return int(expiration_date.timestamp())


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(80), unique=True, nullable=False) 
    email = db.Column(db.String(120), unique=True, nullable=False) 
    _password_hash = db.Column(db.String(100), name='password_hash', nullable=False) 
    _api_key = db.Column(db.String(32), name='api_key', nullable=False, 
                         default=_get_api_token)
    _api_key_expiration_date = db.Column(db.Integer, 
                                         name='api_key_expiration_date', 
                                         nullable=False, 
                                         default=_get_token_expiration_date)
    profile_color = db.Column(db.String(7), nullable=False, default='#ffffff')
    _profile_picture_filename = db.Column(db.String(40), 
                                          name="profile_picture_filename",
                                          nullable=False,
                                          default=active_configuration.DEFAULT_USER_PICTURE_FILENAME)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, passwd: str) -> None:
        self._password_hash = bcrypt.generate_password_hash(passwd).decode('utf-8')

    def check_password(self, passwd: str) -> bool:
        return bcrypt.check_password_hash(self._password_hash, passwd)

    def regenerate_api_token(self) -> None:
        self._api_key = _get_api_token()
        self._api_key_expiration_date = _get_token_expiration_date()
        db.session.commit()

    @property
    def api_token(self) -> str:
        data = {
            'key': self._api_key,
            'exp': self._api_key_expiration_date
        }
        token = jwt.encode(data, active_configuration.SECRET_KEY, 'HS256')
        return token

    @property
    def api_token_expiration_datetime(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self._api_key_expiration_date)

    def __repr__(self):
        return f'<User {self.username}>'

    @classmethod
    def from_api_token(cls, token: str) -> User | API_TOKEN_ERROR:
        try:
            decoded = jwt.decode(token, active_configuration.SECRET_KEY, 'HS256')
        except jwt.DecodeError:
            return API_TOKEN_ERROR.VALIDATION_ERROR
        
        key = decoded.get('key')
        expiration_date = decoded.get('exp')

        # This shouldn't happen
        if key is None or expiration_date is None:
            return API_TOKEN_ERROR.BAD_STRUCTURE

        current_date = datetime.datetime.now().timestamp()
        if current_date > expiration_date:
            return API_TOKEN_ERROR.EXPIRED

        user = User.query.filter_by(_api_key=key).first()
        if user is None:
            return API_TOKEN_ERROR.NOT_FOUND
        else:
            return user

    def _update_username(self, new_username: str):
        self.username = new_username

    def _update_email(self, new_email: str):
        self.email = new_email

    def _update_password(self, new_password: str):
        self.password = new_password

    def _update_profile_color(self, new_profile_color: str):
        if _COLOR_REGEXP.fullmatch(new_profile_color):
            self.profile_color = new_profile_color

    def update_info(self, 
            username: str | None = None, 
            email: str | None = None, 
            password: str | None = None, 
            profile_color: str | None = None,
            profile_picture: FileStorage | None = None, 
        ):
        if username:
            self._update_username(username)

        if email:
            self._update_email(email)

        if password:
            self._update_password(password)

        if profile_color:
            self._update_profile_color(profile_color)

        # TODO 
        if profile_picture:
           ...

        db.session.commit()
