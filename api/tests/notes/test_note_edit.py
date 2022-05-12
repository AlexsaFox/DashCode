from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Note, User
from tests.graphql.edit_note import NOTE_EDIT_QUERY
from tests.notes.test_note_create import get_note_by_id
from tests.utils import GraphQLClient


async def test_note_editing(
    graphql_client: GraphQLClient, token_user: tuple[str, User], note: Note
):
    token, _ = token_user

    data, _ = await graphql_client.get_request_data(
        query=NOTE_EDIT_QUERY,
        variables={
            "note_id": note.id,
            "title": "test_title",
            "content": "test_content",
            "link": "https://testlink.test",
            "is_private": False,
        },
        token=token,
    )
    assert data is not None

    assert data['editNote']['__typename'] == "EditNoteSuccess"
    assert data == {
        "editNote": {
            "__typename": "EditNoteSuccess",
            "note": {
                "id": note.id,
                "title": "test_title",
                "content": "test_content",
                "isPrivate": False,
            },
        }
    }


async def test_note_editing_invalid_id(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
):
    token, _ = token_user

    data, _ = await graphql_client.get_request_data(
        query=NOTE_EDIT_QUERY,
        variables={
            "note_id": "bad_id",
            "title": "test_title",
            "content": "test_content",
            "link": "https://testlink.test",
            "is_private": False,
        },
        token=token,
    )
    assert data is not None

    assert data['editNote']['__typename'] == "RequestValueError"
    assert data == {
        "editNote": {
            "__typename": "RequestValueError",
            "details": "Unable to find a note with provided id",
        }
    }


async def test_note_editing_invalid_owner(
    graphql_client: GraphQLClient, another_token_user: tuple[str, User], note: Note
):
    token, _ = another_token_user

    data, _ = await graphql_client.get_request_data(
        query=NOTE_EDIT_QUERY,
        variables={
            "note_id": note.id,
            "title": "test_title",
            "content": "test_content",
            "link": "https://testlink.test",
            "is_private": False,
        },
        token=token,
    )
    assert data is not None

    assert data['editNote']['__typename'] == "RequestValueError"
    assert data == {
        "editNote": {
            "__typename": "RequestValueError",
            "details": "You haven't got permission to see note with provided id",
        }
    }


async def test_note_editing_bad_title(
    graphql_client: GraphQLClient, token_user: tuple[str, User], note: Note
):
    token, _ = token_user

    data, _ = await graphql_client.get_request_data(
        query=NOTE_EDIT_QUERY,
        variables={
            "note_id": note.id,
            "title": "",
            "content": "test_content",
            "link": "https://testlink.test",
            "is_private": False,
        },
        token=token,
    )
    assert data is not None

    assert data['editNote']['__typename'] == "ValidationError"
    assert data == {
        "editNote": {
            "__typename": "ValidationError",
            "fields": [
                {
                    "field": "title",
                    "details": (
                        "Bad title. Title can't be empty and must contain less than 65"
                        " characters"
                    ),
                }
            ],
        }
    }


async def test_note_editing_bad_content(
    graphql_client: GraphQLClient, token_user: tuple[str, User], note: Note
):
    token, _ = token_user

    data, _ = await graphql_client.get_request_data(
        query=NOTE_EDIT_QUERY,
        variables={
            "note_id": note.id,
            "title": "test_title",
            "content": "",
            "link": "https://testlink.test",
            "is_private": False,
        },
        token=token,
    )
    assert data is not None

    assert data['editNote']['__typename'] == "ValidationError"
    assert data == {
        "editNote": {
            "__typename": "ValidationError",
            "fields": [
                {"field": "content", "details": "Bad content. Content can't be empty"}
            ],
        }
    }


async def test_note_editing_bad_link(
    graphql_client: GraphQLClient, token_user: tuple[str, User], note: Note
):
    token, _ = token_user

    data, _ = await graphql_client.get_request_data(
        query=NOTE_EDIT_QUERY,
        variables={
            "note_id": note.id,
            "title": "test_title",
            "content": "test_content",
            "link": "https://testlink",
            "is_private": False,
        },
        token=token,
    )
    assert data is not None

    assert data['editNote']['__typename'] == "ValidationError"
    assert data == {
        "editNote": {
            "__typename": "ValidationError",
            "fields": [{"field": "link", "details": "Bad link. Link must be valid"}],
        }
    }


async def test_note_editing_no_auth(graphql_client: GraphQLClient, note: Note):

    _, errors = await graphql_client.get_request_data(
        query=NOTE_EDIT_QUERY,
        variables={
            "note_id": note.id,
            "title": "test_title",
            "content": "test_content",
            "link": "https://testlink",
            "is_private": False,
        },
    )
    assert errors is not None

    assert errors[0]['message'] == "Authentication required"
