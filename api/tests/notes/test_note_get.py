from src.db.models import Note, User
from tests.graphql.get_note import NOTE_GET_QUERY
from tests.utils import GraphQLClient


# 1. Owner -> Private note
# 2. Not Owner -> Private note
# 3. Owner -> Public note
# 4. Not Owner -> Public note


async def test_note_receiving_owner_private(
    graphql_client: GraphQLClient, private_note: Note, token_user: tuple[str, User]
):
    token, _ = token_user
    data, _ = await graphql_client.get_request_data(
        query=NOTE_GET_QUERY,
        variables={"id": private_note.id},
        token=token,
    )
    assert data is not None
    assert data == {
        "getNote": {
            "note": {
                "id": private_note.id,
                "title": private_note.title,
                "content": private_note.content,
                "link": private_note.link,
                "isPrivate": private_note.is_private,
                "tags": [tag.content for tag in private_note.tags],
            }
        }
    }


async def test_note_receiving_not_owner_private(
    graphql_client: GraphQLClient,
    private_note: Note,
    another_token_user: tuple[str, User],
):
    token, _ = another_token_user
    data, _ = await graphql_client.get_request_data(
        query=NOTE_GET_QUERY,
        variables={"id": private_note.id},
        token=token,
    )
    assert data is not None
    assert data == {
        "getNote": {"details": "You haven't got access to the note with provided id"}
    }


async def test_note_receiving_owner_public(
    graphql_client: GraphQLClient, note: Note, token_user: tuple[str, User]
):
    token, _ = token_user
    data, _ = await graphql_client.get_request_data(
        query=NOTE_GET_QUERY,
        variables={"id": note.id},
        token=token,
    )
    assert data is not None
    assert data == {
        "getNote": {
            "note": {
                "id": note.id,
                "title": note.title,
                "content": note.content,
                "link": note.link,
                "isPrivate": note.is_private,
                "tags": [tag.content for tag in note.tags],
            }
        }
    }


async def test_note_receiving_not_owner_public(
    graphql_client: GraphQLClient, note: Note, another_token_user: tuple[str, User]
):
    token, _ = another_token_user
    data, _ = await graphql_client.get_request_data(
        query=NOTE_GET_QUERY,
        variables={"id": note.id},
        token=token,
    )
    assert data is not None
    assert data == {
        "getNote": {
            "note": {
                "id": note.id,
                "title": note.title,
                "content": note.content,
                "link": note.link,
                "isPrivate": note.is_private,
                "tags": [tag.content for tag in note.tags],
            }
        }
    }


async def test_note_receiving_invalid_id(
    graphql_client: GraphQLClient, note: Note, token_user: tuple[str, User]
):
    token, _ = token_user
    data, _ = await graphql_client.get_request_data(
        query=NOTE_GET_QUERY,
        variables={"id": "wrong_id"},
        token=token,
    )
    assert data is not None
    assert data == {"getNote": {"details": "Unable to find a note with provided id"}}


async def test_note_receiving_no_auth(graphql_client: GraphQLClient, note: Note):
    _, errors = await graphql_client.get_request_data(
        query=NOTE_GET_QUERY,
        variables={"id": note.id},
    )
    assert errors is not None
    assert errors[0]['message'] == 'Authentication required'
