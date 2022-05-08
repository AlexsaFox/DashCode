import calendar
import re
from datetime import datetime, timedelta
from typing import cast

import bcrypt
from authlib.jose import JWTClaims, jwt
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.session import Session

from src.config import Configuration
from src.db.models import User
from src.types import ExpectedError


class AuthenticationFailedError(ExpectedError):
    def __init__(self, msg: str = 'Unable to find user with provided credentials'):
        super().__init__(msg)


class IdentificationError(ExpectedError):
    def __init__(self, msg: str = 'You must provide username or email'):
        super().__init__(msg)


def authenticate_user(
    session: Session,
    password: str,
    username: str | None = None,
    email: str | None = None,
) -> User:
    if username is None and email is None:
        raise IdentificationError

    user: User | None = (
        session.query(User)
        .filter(or_(User.username == username, User.email == email))
        .first()
    )
    if user is None or not user.check_password(password):
        raise AuthenticationFailedError

    return cast(User, user)


def generate_jwt(config: Configuration, user: User) -> str:
    payload = {
        'iss': config.app.title,
        'sub': str(user.id),
        'username': user.username,
        'exp': datetime.utcnow() + timedelta(hours=config.jwt.expire_hours),
    }
    header = {'alg': config.jwt.algorithm}
    token: bytes = jwt.encode(header, payload, config.secret_key)
    return token.decode()


def decode_jwt(config: Configuration, token: str) -> JWTClaims:
    now = calendar.timegm(datetime.utcnow().utctimetuple())
    claims = jwt.decode(token, config.secret_key)
    claims.validate_exp(now, 0)
    return claims


_INTEGRITY_ERROR_REGEXP = re.compile(
    r'.* duplicate key value violates unique constraint \"(.*)\"\n'
    r'DETAIL:  Key \((.*)\)=\((.*)\) already exists\.'
)


class UserExistsError(ExpectedError):
    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value
        super().__init__(f'User with {field} {value} already exists')


def create_user(
    session: Session,
    username: str,
    email: str,
    password: str,
    is_superuser: bool = False,
) -> User:
    user = User(
        username=username,
        email=email,
        is_superuser=is_superuser,
        password=password,
    )

    try:
        session.add(user)
        session.commit()
        session.refresh(user)
    except IntegrityError as err:
        err_msg = str(err.orig)
        group = _INTEGRITY_ERROR_REGEXP.findall(err_msg)[0]
        column: str = group[1]
        value: str = group[2]
        raise UserExistsError(column, value)

    return user


def delete_user(session: Session, user: User):
    session.add(user)
    session.delete(user)
    session.commit()
