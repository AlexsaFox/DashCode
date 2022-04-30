from typing import Any

from strawberry.permission import BasePermission
from strawberry.types import Info


class IsAuthenticated(BasePermission):
    message = 'Authentication required'

    async def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
        return info.context['user'] is not None
