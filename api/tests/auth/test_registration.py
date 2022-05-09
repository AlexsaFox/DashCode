from src.db.models import User
from tests.graphql.register_user import REGISTRATION_QUERY
from tests.utils import GraphQLClient
from tests.validation.utils import check_validation_error


async def test_registration(graphql_client: GraphQLClient) -> None:
    data, _ = await graphql_client.get_request_data(
        query=REGISTRATION_QUERY,
        variables={
            'username': 'user',
            'email': 'user@user.com',
            'password': 'longandstrongpassword',
        },
    )
    assert data == {
        'registerUser': {
            '__typename': 'RegisterUserSuccess',
            'account': {
                'user': {
                    'username': 'user',
                    'profileColor': '#ffffff',
                    'isSuperuser': False,
                },
                'email': 'user@user.com',
            },
        }
    }


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
