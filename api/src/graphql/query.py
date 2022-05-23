import strawberry
from sqlalchemy.ext.asyncio.session import AsyncSession
from strawberry.types import Info

from src.auth.utils import (
    AuthenticationFailedError,
    IdentificationError,
    authenticate_user,
)
from src.db.models import Note as NoteModel
from src.db.models import User as UserModel
from src.graphql.definitions.errors.request_value_error import RequestValueError
from src.graphql.definitions.note import Note, User
from src.graphql.definitions.pagination import Connection, Cursor, Page
from src.graphql.definitions.responses.get_note import GetNoteResponse, GetNoteSuccess
from src.graphql.definitions.responses.get_public_notes import GetPublicNotesResponse
from src.graphql.definitions.responses.get_token import GetTokenResponse, Token
from src.graphql.definitions.responses.get_user import GetUserResponse, GetUserSuccess
from src.graphql.definitions.user import Account
from src.graphql.permissions.auth import IsAuthenticated
from src.locale.dependencies import Translator
from src.utils.note import NoteNotFoundError, NoteOwnerError, get_note, get_public_notes
from src.utils.user import UserNotFoundError, get_user


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
    ) -> GetTokenResponse:
        session: AsyncSession = info.context['session']
        t: Translator = info.context['translator']

        try:
            user = await session.run_sync(
                authenticate_user, username=username, email=email, password=password
            )
        except AuthenticationFailedError:
            return RequestValueError(t('auth.errors.bad_credentials'))
        except IdentificationError:
            return RequestValueError(t('auth.errors.no_login'))

        return Token.from_user(user, info)

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def get_note(self, info: Info, id: str) -> GetNoteResponse:
        session: AsyncSession = info.context['session']
        t: Translator = info.context['translator']
        user: UserModel = info.context['user']

        try:
            note = await session.run_sync(get_note, id=id, user=user)
        except NoteNotFoundError:
            return RequestValueError(t('notes.errors.note_not_found'))

        except NoteOwnerError:
            return RequestValueError(t('notes.errors.bad_note_owner'))

        return GetNoteSuccess(Note.from_instance(note))

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def get_user(self, info: Info, username: str) -> GetUserResponse:
        session: AsyncSession = info.context['session']
        t: Translator = info.context['translator']

        try:
            user = await session.run_sync(get_user, username=username)
        except UserNotFoundError:
            return RequestValueError(t('users.errors.user_not_found'))

        return GetUserSuccess(User.from_instance(user))

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def get_public_notes(
        self,
        info: Info,
        first: int = 10,
        after: Cursor | None = None,
        newest_first: bool = True,
    ) -> GetPublicNotesResponse:
        session: AsyncSession = info.context['session']
        t: Translator = info.context['translator']

        notes: list[NoteModel]
        try:
            notes = await session.run_sync(
                get_public_notes, after, first + 1, newest_first
            )
        except NoteNotFoundError:
            return RequestValueError(t('notes.errors.note_not_found'))

        has_next_page = len(notes) == first + 1
        edges = [
            Note.from_instance(note).to_edge()
            for note in (notes[:-1] if has_next_page else notes)
        ]

        return Connection(
            page_info=Page(
                has_next_page=has_next_page,
                start_cursor=edges[0].cursor if len(edges) > 0 else None,
                end_cursor=edges[-1].cursor if len(edges) > 0 else None,
            ),
            edges=edges,
        )
