from __future__ import annotations

import re
import os
import jwt
import datetime
from enum import Enum
from flask import url_for
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


def _generate_random_string(size: int, alphabet: str) -> str:
    return ''.join([choice(alphabet) for _ in range(size)])


def _generate_api_token() -> str:
    return _generate_random_string(32, ascii_letters)


def _generate_filename() -> str:
    return _generate_random_string(32, ascii_letters)


def _get_token_expiration_date() -> int:
    current_date = datetime.datetime.now()
    expiration_date = current_date + active_configuration.API_TOKEN_LIFETIME
    return int(expiration_date.timestamp())


def _allowed_file(filename: str) -> bool:
    if '.' not in filename:
        return False
    
    extension = filename.split('.')[-1]
    return extension in active_configuration.ALLOWED_FILE_EXTENSIONS


class InvalidUserPropertyError(Exception):
    """ Raised when user property is attempted to be updated with
    invalid value 
    """
    pass


class User(db.Model):    
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(80), unique=True, nullable=False) 
    email = db.Column(db.String(120), unique=True, nullable=False) 
    _password_hash = db.Column(db.String(100), name='password_hash', nullable=False) 
    _api_key = db.Column(db.String(32), name='api_key', nullable=False, 
                         default=_generate_api_token)
    _api_key_expiration_date = db.Column(db.Integer, 
                                         name='api_key_expiration_date', 
                                         nullable=False, 
                                         default=_get_token_expiration_date)
    profile_color = db.Column(db.String(7), nullable=False, default='#ffffff')
    _profile_picture_filename = db.Column(db.String(40), 
                                          name="profile_picture_filename",
                                          nullable=False,
                                          default=active_configuration.DEFAULT_USER_PICTURE_FILENAME)
    notes = db.relationship('Note', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

    @classmethod
    def from_api_token(cls, token: str) -> User | API_TOKEN_ERROR:
        """ Decodes API token and returns corresponding user or error
        if something goes wrong. Error types:
            VALIDATION_ERROR: unable to validate token. 
                Probably, it's invalid.
            EXPIRED: Token was validated, but it's expired. New token
                for that user must be generated. 
            BAD_STRUCTURE: Token was validated, but it doesn't contain
                'token' or 'exp' fields. This shouldn't happen since
                if token can be validated, then it was created on
                server and therefore has correct structure.
            NOT_FOUND: Token was validated, but user for that token
                can't be found.

        Args:
            token (str): API token

        Returns:
            User | API_TOKEN_ERROR: Corresponding user or error type
        """

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

    @property
    def api_token(self) -> str:
        " User API token"
        data = {
            'key': self._api_key,
            'exp': self._api_key_expiration_date
        }
        token = jwt.encode(data, active_configuration.SECRET_KEY, 'HS256')
        return token

    @property
    def api_token_expiration_datetime(self) -> datetime.datetime:
        """ Exact time on which user token will become unusable and
        must be regenerated.
        """
        return datetime.datetime.fromtimestamp(self._api_key_expiration_date)

    @property
    def password(self):
        """ There's no way to retrieve user password, therefore this
        shouldn't be called.
        """
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, passwd: str) -> None:
        """ Hashes string and stores it as user password. """
        self._password_hash = bcrypt.generate_password_hash(passwd).decode('utf-8')

    @property
    def profile_picture_url(self) -> str:
        return url_for('webapp.uploads.download_file', 
            filename=self._profile_picture_filename)

    def check_password(self, passwd: str) -> bool:
        """ Checks if provided string matches user password. """   
        return bcrypt.check_password_hash(self._password_hash, passwd)

    def regenerate_api_token(self) -> None:
        """ Regenerates API token for this user. """
        self._api_key = _generate_api_token()
        self._api_key_expiration_date = _get_token_expiration_date()
        db.session.commit()

    def update_info(self, *args, **kwargs ) -> list[str]:
        """ Updates information about user and saves changes to
        database. All arguments MUST be passed with keywords. If
        argument is None or empty value (for example, empty string),
        changes to that field will not be applied. If any errors occur
        while updating information (for example, if invalid value is
        passed), changes to that field will not be made, but all other
        changes will be applied. 

        Args:
            username (str | None, optional): New username.
            email (str | None, optional): New email.
            password (str | None, optional): New password.
            profile_color (str | None, optional): New profile color.
            profile_picture (FileStorage | None, optional): New profile picture.

        Raises:
            ValueError: no matching property update handler was found
                for keyword argument.

        Returns:
            list[str]: List of errors that occured while updating information.
        """

        errors = []
        property_changer_name_template = '_update_{property}'

        for property, value in kwargs.items():
            if value:
                try:
                    property_changer_name = property_changer_name_template.format(
                        property=property)
                    property_changer =  getattr(self, property_changer_name)
                except AttributeError:
                    raise ValueError(
                        f'no handler for updating "{property}" is defined'
                    )

                try:
                    property_changer(value)
                except InvalidUserPropertyError as err:
                    errors.append(err.args[0])

        db.session.commit()
        return errors

    def _update_username(self, new_username: str):
        self.username = new_username

    def _update_email(self, new_email: str):
        self.email = new_email

    def _update_password(self, new_password: str):
        self.password = new_password

    def _update_profile_color(self, new_profile_color: str):
        if not _COLOR_REGEXP.fullmatch(new_profile_color):
            raise InvalidUserPropertyError(
                f'Color format is invalid. Expected "#rrggbb" value'
                f'(with "#"), where all values are hexadecimal digits'
            )

        self.profile_color = new_profile_color.upper()

    def _update_profile_picture(self, new_profile_picture: FileStorage):
        filename = new_profile_picture.filename
        if not _allowed_file(filename):
            raise InvalidUserPropertyError(
                'This file extension is not allowed. You can upload only '
                + ', '.join(active_configuration.ALLOWED_FILE_EXTENSIONS)
                + ' files'
            )

        default_filename = active_configuration.DEFAULT_USER_PICTURE_FILENAME
        if self._profile_picture_filename == default_filename:
            filename_base = _generate_filename()
        else:
            last_dot = self._profile_picture_filename.rindex('.')
            filename_base = self._profile_picture_filename[:last_dot]

            # Remove old profile picture, if it is not default 
            old_path = os.path.join(active_configuration.UPLOAD_FOLDER,
                                    self._profile_picture_filename
                                    )
            os.remove(old_path)

        # If this line is being executed, then filename passed 
        # _allowed_file(filename) check and therefore contains
        # '.' character, so IndexError won't occur
        extension = filename.split('.')[-1]
        saved_filename = filename_base + '.' + extension
        save_path = os.path.join(active_configuration.UPLOAD_FOLDER, 
                                 saved_filename)
        new_profile_picture.save(save_path)
        self._profile_picture_filename = saved_filename
