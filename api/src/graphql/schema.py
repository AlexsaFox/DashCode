from aioredis import Redis
import strawberry

from typing import Any, Callable

from fastapi import Depends
from graphql import GraphQLError
from strawberry.types import ExecutionContext
from strawberry.fastapi import GraphQLRouter
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.auth.dependencies import get_user_or_none
from src.cache.dependencies import get_cache
from src.config import Configuration
from src.db.dependencies import get_session
from src.db.models import User as UserModel
from src.dependencies import get_config
from src.graphql.query import Query
from src.graphql.mutation import Mutation
from src.locale.dependencies import get_translator
from src.types import ExpectedError


async def get_context(
    user: UserModel | None = Depends(get_user_or_none),
    cache: Redis = Depends(get_cache),
    config: Configuration = Depends(get_config),
    session: AsyncSession = Depends(get_session),
    translator: Callable[[str, Any], str] = Depends(get_translator),
) -> dict[str, Any]:
    return {
        'user': user,
        'cache': cache,
        'config': config,
        'session': session,
        'translator': translator,
    }


class StrawberrySchema(strawberry.Schema):
    '''
    Same as `strawberry.Schema`, but overrides `proccess_errors` method
    to silence permission errors and expected errors in console
    '''

    SILENCED_ERR_TYPES = (PermissionError, ExpectedError)

    def process_errors(
        self,
        errors: list[GraphQLError],
        execution_context: ExecutionContext | None = None,
    ) -> None:
        not_silenced_errors: list[GraphQLError] = [
            err
            for err in errors
            if not issubclass(type(err.original_error), self.SILENCED_ERR_TYPES)
        ]
        super().process_errors(not_silenced_errors, execution_context)


schema = StrawberrySchema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema, context_getter=get_context)
