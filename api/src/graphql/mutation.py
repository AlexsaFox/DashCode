import strawberry

from strawberry.types import Info
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.auth.utils import UserExistsError, create_user
from src.graphql.definitions.user import User
from src.graphql.definitions.register_user_response import (
    RegisterUserResponse,
    RegisterUserSuccess,
    UserAlreadyExists,
)


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def register_user(
        self, info: Info, username: str, email: str, password: str
    ) -> RegisterUserResponse:
        session: AsyncSession = info.context['session']

        try:
            user = await session.run_sync(
                create_user, username=username, email=email, password=password
            )
            return RegisterUserSuccess(User.from_instance(user))
        except UserExistsError as err:
            return UserAlreadyExists(field=err.field, value=err.value)
