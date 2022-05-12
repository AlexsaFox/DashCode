from functools import wraps
from typing import Any, Callable

from strawberry.permission import BasePermission
from strawberry.types import Info

from src.locale.dependencies import Translator


class LocalizedPermission(BasePermission):
    message_code: str

    @staticmethod
    def localize(func: Callable) -> Callable:
        @wraps(func)
        def inner(self, source: Any, info: Info, **kwargs):
            t: Translator = info.context['translator']
            self.message = t(self.message_code)
            return func(self, source, info, **kwargs)

        return inner
