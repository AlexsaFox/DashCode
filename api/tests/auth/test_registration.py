from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from src.db.models import User
from tests.auth.utils import try_credentials
from tests.graphql.register_user import REGISTRATION_QUERY
from tests.utils import GraphQLClient
from tests.validation.utils import check_validation_error


async def test_registration(
    graphql_client: GraphQLClient,
    database_session: AsyncSession,
    database_engine: AsyncEngine,
) -> None:
    data, _ = await graphql_client.get_request_data(
        query=REGISTRATION_QUERY,
        variables={
            'username': 'user',
            'email': 'user@user.com',
            'password': 'longandstrongpassword',
        },
    )

    query = await database_session.execute(select(User).filter_by(username='user'))
    row = query.first()
    assert row is not None
    user: User = row[0]

    assert data == {
        'registerUser': {
            '__typename': 'RegisterUserSuccess',
            'account': {
                'username': user.username,
                'email': user.email,
                'profileColor': user.profile_color,
                'isSuperuser': user.is_superuser,
                'profilePictureFilename': user.profile_picture_filename,
                'notes': [],
            },
        }
    }

    assert await try_credentials(database_engine, user.email, 'longandstrongpassword')


async def test_registration_duplicate_username(
    graphql_client: GraphQLClient, user: User
) -> None:
    data, _ = await graphql_client.get_request_data(
        query=REGISTRATION_QUERY,
        variables={
            'username': user.username,
            'email': 'unique' + user.email,
            'password': 'longandstrongpassword',
        },
    )
    assert data == {
        'registerUser': {
            '__typename': 'UserAlreadyExists',
            'field': 'username',
            'value': user.username,
        }
    }


async def test_registration_duplicate_email(
    graphql_client: GraphQLClient, user: User
) -> None:
    data, _ = await graphql_client.get_request_data(
        query=REGISTRATION_QUERY,
        variables={
            'username': 'unique' + user.username,
            'email': user.email,
            'password': 'longandstrongpassword',
        },
    )
    assert data == {
        'registerUser': {
            '__typename': 'UserAlreadyExists',
            'field': 'email',
            'value': user.email,
        }
    }


async def test_registration_invalid_username(graphql_client: GraphQLClient) -> None:
    data, _ = await graphql_client.get_request_data(
        query=REGISTRATION_QUERY,
        variables={
            'username': 'i am invalid :)',
            'email': 'valid@email.wow',
            'password': 'longandstrongpassword',
        },
    )
    assert data is not None
    check_validation_error(data['registerUser'], ['username'])


async def test_registration_invalid_email(graphql_client: GraphQLClient) -> None:
    data, _ = await graphql_client.get_request_data(
        query=REGISTRATION_QUERY,
        variables={
            'username': 'i_am_valid',
            'email': 'invalid...',
            'password': 'longandstrongpassword',
        },
    )
    assert data is not None
    check_validation_error(data['registerUser'], ['email'])


async def test_registration_invalid_password(graphql_client: GraphQLClient) -> None:
    data, _ = await graphql_client.get_request_data(
        query=REGISTRATION_QUERY,
        variables={
            'username': 'i_am_valid',
            'email': 'valid@email.wow',
            'password': 'short:(',
        },
    )
    assert data is not None
    check_validation_error(data['registerUser'], ['password'])


async def test_registration_multiple_bad(graphql_client: GraphQLClient) -> None:
    data, _ = await graphql_client.get_request_data(
        query=REGISTRATION_QUERY,
        variables={
            'username': 'i am invalid',
            'email': 'invalid...',
            'password': 'short:(',
        },
    )
    assert data is not None
    check_validation_error(data['registerUser'], ['username', 'email', 'password'])
