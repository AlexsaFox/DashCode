import strawberry
from sqlalchemy.ext.asyncio.session import AsyncSession
from strawberry.types import Info

from src.auth.utils import UserExistsError, create_user
from src.db.models import Note as NoteModel
from src.db.models import User as UserModel
from src.db.validation import ModelFieldValidationError
from src.graphql.definitions.note import Note
from src.graphql.definitions.register_user_response import (
    RegisterUserResponse,
    RegisterUserSuccess,
    UserAlreadyExists,
)
from src.graphql.definitions.user import User
from src.graphql.definitions.validation_error import FieldError, ValidationError
from src.graphql.permissions.auth import IsAuthenticated
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
            return RegisterUserSuccess(User.from_instance(user))
        except ModelFieldValidationError as err:
            error_fields = [
                FieldError(field=field, details=t(f'validation.user.errors.{field}'))
                for field in err.fields
            ]
            return ValidationError(error_fields)
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
