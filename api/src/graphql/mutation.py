import strawberry
from sqlalchemy.ext.asyncio.session import AsyncSession
from strawberry.types import Info

from src.auth.utils import UserExistsError, create_user, delete_user
from src.db.models import Note as NoteModel
from src.db.models import User as UserModel
from src.db.validation import ModelFieldValidationError
from src.graphql.definitions.errors.validation_error import FieldError, ValidationError
from src.graphql.definitions.note import Note
from src.graphql.definitions.responses.delete_user import (
    DeleteUserResponse,
    DeleteUserSuccess,
)
from src.graphql.definitions.responses.register_user import (
    RegisterUserResponse,
    RegisterUserSuccess,
    UserAlreadyExists,
)
from src.graphql.definitions.user import Account, User
from src.graphql.permissions.auth import IsAuthenticated
from src.graphql.permissions.require_password import requires_password
from src.locale.dependencies import Translator
from src.utils.note import create_note


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def register_user(
        self, info: Info, username: str, email: str, password: str
    ) -> RegisterUserResponse:
        session: AsyncSession = info.context['session']
        t: Translator = info.context['translator']

        try:
            user = await session.run_sync(
                create_user, username=username, email=email, password=password
            )
            return RegisterUserSuccess(Account.from_instance(user))
        except ModelFieldValidationError as err:
            error_fields = [
                FieldError(field=field, details=t(f'validation.user.errors.{field}'))
                for field in err.fields
            ]
            return ValidationError(error_fields)
        except UserExistsError as err:
            return UserAlreadyExists(field=err.field, value=err.value)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    @requires_password
    async def delete_user(self, info: Info, password: str) -> DeleteUserResponse:
        session: AsyncSession = info.context['session']
        user: UserModel = info.context['user']

        await session.run_sync(delete_user, user)
        return DeleteUserSuccess(account=Account.from_instance(user))

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
