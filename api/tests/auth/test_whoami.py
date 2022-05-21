from src.db.models import Note, User
from tests.auth.utils import check_auth
from tests.graphql.whoami import WHOAMI_QUERY
from tests.utils import GraphQLClient


async def test_whoami(graphql_client: GraphQLClient, token_user: tuple[str, User]):
    token, user = token_user

    data, _ = await graphql_client.get_request_data(query=WHOAMI_QUERY, token=token)
    assert data is not None

    user_data = data['whoami']
    assert user_data == {
        'username': user.username,
        'email': user.email,
        'profileColor': user.profile_color,
        'isSuperuser': user.is_superuser,
        'profilePictureFilename': user.profile_picture_filename,
        'notes': [],
    }


async def test_whoami_with_public_note(
    graphql_client: GraphQLClient, token_user: tuple[str, User], note: Note
):
    token, user = token_user

    data, _ = await graphql_client.get_request_data(query=WHOAMI_QUERY, token=token)
    assert data is not None

    user_data = data['whoami']
    assert user_data == {
        'username': user.username,
        'email': user.email,
        'profileColor': user.profile_color,
        'isSuperuser': user.is_superuser,
        'profilePictureFilename': user.profile_picture_filename,
        'notes': [{'id': note.id}],
    }


async def test_whoami_with_private_note(
    graphql_client: GraphQLClient, token_user: tuple[str, User], private_note: Note
):
    token, user = token_user

    data, _ = await graphql_client.get_request_data(query=WHOAMI_QUERY, token=token)
    assert data is not None

    user_data = data['whoami']
    assert user_data == {
        'username': user.username,
        'email': user.email,
        'profileColor': user.profile_color,
        'isSuperuser': user.is_superuser,
        'profilePictureFilename': user.profile_picture_filename,
        'notes': [{'id': private_note.id}],
    }


async def test_whoami_no_auth(graphql_client: GraphQLClient):
    data, errors = await graphql_client.get_request_data(query=WHOAMI_QUERY)
    check_auth(data, errors)
