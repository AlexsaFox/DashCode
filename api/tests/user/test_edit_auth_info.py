from sqlalchemy.ext.asyncio import AsyncEngine

from src.db.models import User
from tests.auth.utils import check_auth_error, try_credentials
from tests.graphql.edit_account_auth import EDIT_ACCOUNT_AUTH_QUERY
from tests.utils import GraphQLClient
from tests.validation.utils import check_validation_error


async def test_edit_email(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    database_engine: AsyncEngine,
):
    token, _ = token_user
    new_email = 'different@email.com'

    data, _ = await graphql_client.get_request_data(
        query=EDIT_ACCOUNT_AUTH_QUERY,
        variables={
            'password': 'password',
            'newEmail': new_email,
        },
        token=token,
    )
    assert data is not None
    assert data['editAccountAuth']['__typename'] == 'EditAccountSuccess'
    assert data['editAccountAuth']['account']['email'] == new_email

    assert await try_credentials(database_engine, new_email, 'password')


async def test_edit_email_exists(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    database_engine: AsyncEngine,
    another_user: User,
):
    token, _ = token_user

    data, _ = await graphql_client.get_request_data(
        query=EDIT_ACCOUNT_AUTH_QUERY,
        variables={
            'password': 'password',
            'newEmail': another_user.email,
        },
        token=token,
    )
    assert data is not None
    assert data['editAccountAuth'] == {
        '__typename': 'UserAlreadyExists',
        'field': 'email',
        'value': another_user.email,
    }
    assert not await try_credentials(database_engine, another_user.email, 'password')


async def test_edit_email_invalid_data(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    database_engine: AsyncEngine,
):
    token, _ = token_user
    new_email = 'he-he-he >:)'

    data, _ = await graphql_client.get_request_data(
        query=EDIT_ACCOUNT_AUTH_QUERY,
        variables={
            'password': 'password',
            'newEmail': new_email,
        },
        token=token,
    )
    assert data is not None
    check_validation_error(data['editAccountAuth'], ['email'])
    assert not await try_credentials(database_engine, new_email, 'password')


async def test_edit_password(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    database_engine: AsyncEngine,
):
    token, old_user = token_user
    new_password = 'https://www.youtube.com/watch?v=iik25wqIuFo'

    data, _ = await graphql_client.get_request_data(
        query=EDIT_ACCOUNT_AUTH_QUERY,
        variables={
            'password': 'password',
            'newPassword': new_password,
        },
        token=token,
    )
    assert data is not None
    assert data['editAccountAuth']['__typename'] == 'EditAccountSuccess'
    assert data['editAccountAuth']['account']['email'] == old_user.email

    assert await try_credentials(database_engine, old_user.email, new_password)


async def test_edit_password_invalid_data(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    database_engine: AsyncEngine,
):
    token, old_user = token_user
    new_password = 'short:('

    data, _ = await graphql_client.get_request_data(
        query=EDIT_ACCOUNT_AUTH_QUERY,
        variables={
            'password': 'password',
            'newPassword': new_password,
        },
        token=token,
    )
    assert data is not None
    check_validation_error(data['editAccountAuth'], ['password'])
    assert not await try_credentials(database_engine, old_user.email, new_password)


async def test_edit_all(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    database_engine: AsyncEngine,
):
    token, _ = token_user
    new_email = 'different@email.com'
    new_password = 'https://www.youtube.com/watch?v=iik25wqIuFo'

    data, _ = await graphql_client.get_request_data(
        query=EDIT_ACCOUNT_AUTH_QUERY,
        variables={
            'password': 'password',
            'newEmail': new_email,
            'newPassword': new_password,
        },
        token=token,
    )
    assert data is not None
    assert data['editAccountAuth']['__typename'] == 'EditAccountSuccess'
    assert data['editAccountAuth']['account']['email'] == new_email

    assert await try_credentials(database_engine, new_email, new_password)


async def test_edit_bad_password(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    database_engine: AsyncEngine,
):
    token, _ = token_user
    new_email = 'different@email.com'

    data, _ = await graphql_client.get_request_data(
        query=EDIT_ACCOUNT_AUTH_QUERY,
        variables={
            'password': 'never gonna give you up',
            'newEmail': new_email,
        },
        token=token,
    )
    assert data is not None
    assert data['editAccountAuth']['__typename'] == 'RequestValueError'
    assert data['editAccountAuth']['details'] == 'Wrong password'

    assert not await try_credentials(database_engine, new_email, 'password')


async def test_edit_no_auth(
    graphql_client: GraphQLClient,
):
    new_email = 'different@email.com'

    data, errors = await graphql_client.get_request_data(
        query=EDIT_ACCOUNT_AUTH_QUERY,
        variables={
            'password': 'never gonna give you up',
            'newEmail': new_email,
        },
    )
    check_auth_error(data, errors)
