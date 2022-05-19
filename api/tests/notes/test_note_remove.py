from typing import Any

from sqlalchemy.ext.asyncio import AsyncEngine

from src.db.models import Note, User
from tests.graphql.remove_note import NOTE_REMOVE_QUERY
from tests.notes.test_note_create import get_note_by_id
from tests.utils import GraphQLClient


async def test_note_removing(
    graphql_client: GraphQLClient,
    database_engine: AsyncEngine,
    token_user: tuple[str, User],
    note: Note,
):
    token, _ = token_user
    data, _ = await graphql_client.get_request_data(
        query=NOTE_REMOVE_QUERY,
        variables={"id": note.id},
        token=token,
    )

    assert data is not None
    assert data['removeNote']['__typename'] == "RemoveNoteSuccess"

    assert await get_note_by_id(database_engine, note.id) is None


async def test_note_removing_invalid_owner(
    graphql_client: GraphQLClient,
    database_engine: AsyncEngine,
    another_token_user: tuple[str, User],
    note: Note,
):
    token, _ = another_token_user
    data, _ = await graphql_client.get_request_data(
        query=NOTE_REMOVE_QUERY,
        variables={"id": note.id},
        token=token,
    )

    assert data is not None
    assert data['removeNote']['__typename'] == "RequestValueError"
    assert (
        data['removeNote']['details']
        == "You haven't got access to the note with provided id"
    )

    assert await get_note_by_id(database_engine, note.id) is not None


async def test_note_removing_invalid_id(
    graphql_client: GraphQLClient,
    database_engine: AsyncEngine,
    token_user: tuple[str, User],
    note: Note,
):
    token, _ = token_user
    data, _ = await graphql_client.get_request_data(
        query=NOTE_REMOVE_QUERY,
        variables={"id": "hehe"},
        token=token,
    )

    assert data is not None
    assert data['removeNote']['__typename'] == "RequestValueError"
    assert data['removeNote']['details'] == "Unable to find a note with provided id"

    assert await get_note_by_id(database_engine, note.id) is not None
