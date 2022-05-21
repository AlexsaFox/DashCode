from sqlalchemy import select
from sqlalchemy.engine.row import Row
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from src.db.models import Note, Tag, User
from src.utils.note import create_note
from tests.graphql.remove_note import NOTE_REMOVE_QUERY
from tests.notes.test_note_create import get_note_by_id
from tests.utils import GraphQLClient


async def tag_exists_in_db(engine: AsyncEngine, tag_content: str) -> bool:
    async with AsyncSession(engine) as session:
        tag_row: Row | None = (
            await session.execute(select(Tag).filter(Tag.content == tag_content))
        ).one_or_none()
    return tag_row is not None


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

    for tag in note.tags:
        assert not await tag_exists_in_db(database_engine, tag.content)


async def test_note_removing_tag_exists_in_other(
    graphql_client: GraphQLClient,
    database_engine: AsyncEngine,
    database_session: AsyncSession,
    token_user: tuple[str, User],
    note: Note,
):
    token, user = token_user

    await database_session.run_sync(
        create_note,
        'title',
        'content',
        ['pytest', 'fixture'],
        'http://google.com',
        True,
        user,
    )

    data, _ = await graphql_client.get_request_data(
        query=NOTE_REMOVE_QUERY,
        variables={"id": note.id},
        token=token,
    )

    assert data is not None
    assert data['removeNote']['__typename'] == "RemoveNoteSuccess"

    assert await get_note_by_id(database_engine, note.id) is None

    for should_not_exist in ['testing']:
        assert not await tag_exists_in_db(database_engine, should_not_exist)

    for should_exist in ['pytest', 'fixture']:
        assert await tag_exists_in_db(database_engine, should_exist)


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
