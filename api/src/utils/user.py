from typing import cast

from sqlalchemy.orm.session import Session

from src.db.models import User
from src.types import ExpectedError


def get_user(session: Session, username: str) -> User:
    user = session.query(User).filter(User.username == username).first()

    if user is None:
        raise UserNotFoundError
    return cast(User, user)


class UserNotFoundError(ExpectedError):
    def __init__(self, msg: str = 'Unable to find a user with provided username'):
        super().__init__(msg)
