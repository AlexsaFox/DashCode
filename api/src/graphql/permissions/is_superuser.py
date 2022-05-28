from typing import Any

from strawberry.types import Info

from src.db.models import User
from src.graphql.permissions.locale import LocalizedPermission


class IsSuperuser(LocalizedPermission):
    message_code = 'auth.errors.not_superuser'

    @LocalizedPermission.localize
    async def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
        user: User = info.context['user']
        return user.is_superuser
