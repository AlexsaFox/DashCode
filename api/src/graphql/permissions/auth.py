from typing import Any

from strawberry.types import Info
from src.graphql.permissions.locale import LocalizedPermission


class IsAuthenticated(LocalizedPermission):
    message_code = 'errors.auth.no_auth'

    @LocalizedPermission.localize
    async def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
        return info.context['user'] is not None
