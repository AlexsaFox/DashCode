from functools import wraps
from typing import Callable

from strawberry.types import Info

from src.db.models import User as UserModel
from src.graphql.definitions.errors.request_value_error import RequestValueError
from src.locale.dependencies import Translator


def requires_password(func: Callable) -> Callable:
    @wraps(func)
    async def password_check(self, info: Info, password: str, **kwargs):
        user: UserModel = info.context['user']
        t: Translator = info.context['translator']

        if not user.check_password(password):
            return RequestValueError(t('auth.errors.require_password.wrong_password'))
        return await func(self, info=info, password=password, **kwargs)

    return password_check
