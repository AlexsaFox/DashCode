import strawberry
from sqlalchemy.ext.asyncio.session import AsyncSession
from strawberry.types import Info

from src.auth.utils import (
    AuthenticationFailedError,
    UsernameOrEmailNotProvidedError,
    authenticate_user,
)
from src.db.models import User as UserModel
from src.graphql.definitions.token import Token
from src.graphql.definitions.user import Account
from src.graphql.permissions.auth import IsAuthenticated
from src.locale.dependencies import Translator


@strawberry.type
class Query:
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def whoami(self, info: Info) -> Account:
        user: UserModel = info.context['user']
        return Account.from_instance(user)

    @strawberry.field
    async def token(
        self,
        info: Info,
        password: str,
        username: str | None = None,
        email: str | None = None,
    ) -> Token | None:
        session: AsyncSession = info.context['session']
        t: Translator = info.context['translator']

        try:
            user = await session.run_sync(
                authenticate_user, username=username, email=email, password=password
            )
        except AuthenticationFailedError:
            raise AuthenticationFailedError(t('auth.errors.bad_credentials'))
        except UsernameOrEmailNotProvidedError:
            raise UsernameOrEmailNotProvidedError(t('auth.errors.no_login'))

        return Token.from_user(user, info)
