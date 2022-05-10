from src.db.models import Note, User
from tests.graphql.get_note import NOTE_GET_QUERY
from tests.utils import GraphQLClient


async def test_note_receiving(
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


async def test_note_receiving_invalid_owner(
    graphql_client: GraphQLClient, another_token_user: tuple[str, User], note: Note
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
            "details": "You haven't got permission to see note with provided id"
        }
    }


async def test_note_receiving_no_auth(graphql_client: GraphQLClient, note: Note):
    _, errors = await graphql_client.get_request_data(
        query=NOTE_GET_QUERY,
        variables={"id": note.id},
    )
    assert errors is not None
    assert errors[0]['message'] == 'Authentication required'
