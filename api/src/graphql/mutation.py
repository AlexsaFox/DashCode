import strawberry

from strawberry.types import Info
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.auth.utils import UserExistsError, create_user
from src.utils.note import create_note
from src.db.models import User as UserModel, Note as NoteModel
from src.graphql.permissions.auth import IsAuthenticated
from src.graphql.definitions.user import User
from src.graphql.definitions.note import Note
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

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def create_note(
        self,
        info: Info,
        title: str,
        content: str,
        link: str = "",
        is_private: bool = True,
    ) -> Note:
        session: AsyncSession = info.context['session']
        user: UserModel = info.context['user']

        note: NoteModel = await session.run_sync(
            create_note, title, content, link, is_private, user
        )
        return Note.from_instance(note)
