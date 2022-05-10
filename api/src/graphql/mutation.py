from typing import Optional

import strawberry
from sqlalchemy.ext.asyncio.session import AsyncSession
from strawberry.file_uploads import Upload
from strawberry.types import Info

from src.auth.utils import UserExistsError, create_user, delete_user
from src.config import Configuration
from src.db.models import Note as NoteModel
from src.db.models import User as UserModel
from src.db.utils import save_file
from src.db.validation import (
    FileBadExtensionError,
    FileBadMimeTypeError,
    FileTooLargeError,
    ModelFieldValidationError,
)
from src.graphql.definitions.errors.request_value_error import RequestValueError
from src.graphql.definitions.errors.validation_error import ValidationError
from src.graphql.definitions.note import Note
from src.graphql.definitions.responses.create_note import CreateNoteResponse
from src.graphql.definitions.responses.delete_user import (
    DeleteUserResponse,
    DeleteUserSuccess,
)
from src.graphql.definitions.responses.edit_account import (
    EditAccountResponse,
    EditAccountSuccess,
)
from src.graphql.definitions.responses.register_user import (
    RegisterUserResponse,
    RegisterUserSuccess,
    UserAlreadyExists,
)
from src.graphql.definitions.user import Account
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
            return ValidationError.from_exception(err, t)
        except UserExistsError as err:
            return UserAlreadyExists(field=err.field, value=err.value)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    @requires_password
    async def edit_account_auth(
        self,
        info: Info,
        password: str,
        new_password: str | None = None,
        new_email: str | None = None,
    ) -> EditAccountResponse:
        session: AsyncSession = info.context['session']
        user: UserModel = info.context['user']
        t: Translator = info.context['translator']

        try:
            await session.run_sync(
                user.update_fields, email=new_email, password=new_password
            )
            return EditAccountSuccess(Account.from_instance(user))
        except ModelFieldValidationError as err:
            return ValidationError.from_exception(err, t)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def edit_account(
        self,
        info: Info,
        new_username: str | None = None,
        new_profile_color: str | None = None,
        new_profile_picture: Optional[Upload] = None,  # Upload | None returns error
    ) -> EditAccountResponse:
        session: AsyncSession = info.context['session']
        user: UserModel = info.context['user']
        config: Configuration = info.context['config']
        t: Translator = info.context['translator']

        try:
            user.validate_fields(username=new_username, profile_color=new_profile_color)

            new_profile_picture_filename = None
            if new_profile_picture is not None:
                new_profile_picture_filename = await save_file(
                    config.file_upload, new_profile_picture
                )

            await session.run_sync(
                user.update_fields,
                username=new_username,
                profile_color=new_profile_color,
                profile_picture_filename=new_profile_picture_filename,
                validate=False,
            )
            return EditAccountSuccess(Account.from_instance(user))
        except ModelFieldValidationError as err:
            return ValidationError.from_exception(err, t)
        except FileTooLargeError as err:
            return RequestValueError(t('validation.errors.user.upload_file.too_large'))
        except FileBadExtensionError as err:
            return RequestValueError(
                t('validation.errors.user.upload_file.bad_extension')
            )
        except FileBadMimeTypeError as err:
            return RequestValueError(
                t('validation.errors.user.upload_file.bad_mime_type')
            )

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
    ) -> CreateNoteResponse:
        session: AsyncSession = info.context['session']
        user: UserModel = info.context['user']
        t: Translator = info.context['translator']
        try:
            note: NoteModel = await session.run_sync(
                create_note, title, content, link, is_private, user
            )
        except ModelFieldValidationError as err:
            return ValidationError.from_exception(err, t)

        return Note.from_instance(note)
