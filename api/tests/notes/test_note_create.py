from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Note, User
from tests.graphql.create_note import NOTE_CREATE_QUERY
from tests.utils import GraphQLClient


async def get_note_by_id(session: AsyncSession, note_id: str) -> Note | None:
    query = await session.execute(select(Note).filter_by(id=note_id))
    row = query.first()
    if row is None:
        return None
    return row[0]


async def test_note_creation(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    database_session: AsyncSession,
):
    token, _ = token_user

    data, _ = await graphql_client.get_request_data(
        query=NOTE_CREATE_QUERY,
        variables={
            "title": "blabla",
            "content": "blablabla",
            "link": "https://google.com",
            "is_private": True,
        },
        token=token,
    )
    assert data is not None

    note_id = data['createNote']['id']

    assert data == {
        "createNote": {
            "id": note_id,
            "title": "blabla",
            "content": "blablabla",
            "isPrivate": True,
        }
    }
    assert await get_note_by_id(database_session, note_id) is not None


async def test_note_creation_invalid_title(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
):
    token, _ = token_user

    data, _ = await graphql_client.get_request_data(
        query=NOTE_CREATE_QUERY,
        variables={
            "title": "",
            "content": "blablabla",
            "link": "https://google.com",
            "is_private": True,
        },
        token=token,
    )
    assert data is not None
    assert data == {
        "createNote": {
            "fields": [
                {
                    "field": "title",
                    "details": (
                        "Bad title. Title can't be empty and must contain less than 65"
                        " characters"
                    ),
                }
            ]
        }
    }


async def test_note_creation_invalid_content(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
):
    token, _ = token_user

    data, _ = await graphql_client.get_request_data(
        query=NOTE_CREATE_QUERY,
        variables={
            "title": "blabla",
            "content": "",
            "link": "https://google.com",
            "is_private": True,
        },
        token=token,
    )
    assert data is not None
    assert data == {
        "createNote": {
            "fields": [
                {"field": "content", "details": "Bad content. Content can't be empty"}
            ]
        }
    }


async def test_note_creation_invalid_link(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
):
    token, _ = token_user

    data, _ = await graphql_client.get_request_data(
        query=NOTE_CREATE_QUERY,
        variables={
            "title": "blabla",
            "content": "blablabla",
            "link": "https://1",
            "is_private": True,
        },
        token=token,
    )
    assert data is not None
    assert data == {
        "createNote": {
            "fields": [{"field": "link", "details": "Bad link. Link must be valid"}]
        }
    }


async def test_note_creation_no_auth(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
):
    _, errors = await graphql_client.get_request_data(
        query=NOTE_CREATE_QUERY,
        variables={
            "title": "blabla",
            "content": "blablabla",
            "link": "https://1",
            "is_private": True,
        },
    )
    assert errors is not None
    assert errors[0]['message'] == 'Authentication required'
