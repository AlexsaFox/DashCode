import strawberry

from strawberry.types import Info
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.auth.utils import authenticate_user
from src.db.models import User as UserModel
from src.graphql.auth import IsAuthenticated
from src.graphql.definitions.token import Token
from src.graphql.definitions.user import User


@strawberry.type
class Query:
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def whoami(self, info: Info) -> User:
        user: UserModel = info.context['user']
        return User.from_instance(user)

    @strawberry.field
    async def token(
        self,
        info: Info,
        password: str,
        username: str | None = None,
        email: str | None = None,
    ) -> Token | None:
        session: AsyncSession = info.context['session']
        # Might raise `AuthenticationFailedError` or `UsernameOrEmailNotProvidedError`.
        # If that happens, error will be passed in `errors`` section of GraphQL response.
        # Token value in that case will remain null.
        user = await session.run_sync(
            authenticate_user, username=username, email=email, password=password
        )
        return Token.from_user(user, info)
