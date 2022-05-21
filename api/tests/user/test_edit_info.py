from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from src.auth.utils import AuthenticationFailedError, authenticate_user
from src.db.models import User
from tests.auth.utils import check_auth
from tests.graphql.edit_account import EDIT_ACCOUNT_QUERY
from tests.utils import GraphQLClient
from tests.validation.utils import check_validation_error


async def try_changes(
    engine: AsyncEngine,
    username: str,
    profile_color: str | None = None,
) -> bool:
    try:
        async with AsyncSession(engine) as session:
            user = await session.run_sync(
                authenticate_user, password='password', username=username
            )

        if profile_color != None:
            assert user.profile_color == profile_color
        return True
    except (AssertionError, AuthenticationFailedError):
        return False


async def test_edit_username(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    database_engine: AsyncEngine,
):
    token, _ = token_user
    new_username = '3L1T3_H4X0R_1337'

    data, _ = await graphql_client.get_request_data(
        query=EDIT_ACCOUNT_QUERY,
        variables={
            'newUsername': new_username,
        },
        token=token,
    )
    assert data is not None
    assert data['editAccount']['__typename'] == 'EditAccountSuccess'
    assert data['editAccount']['account']['username'] == new_username
    assert await try_changes(database_engine, new_username)


async def test_edit_username_exists(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    database_engine: AsyncEngine,
    another_user: User,
):
    token, _ = token_user

    data, _ = await graphql_client.get_request_data(
        query=EDIT_ACCOUNT_QUERY,
        variables={
            'newUsername': another_user.username,
        },
        token=token,
    )
    assert data is not None
    assert data['editAccount'] == {
        '__typename': 'UserAlreadyExists',
        'field': 'username',
        'value': another_user.username,
    }
    assert not await try_changes(database_engine, another_user.username)


async def test_edit_username_invalid_data(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    database_engine: AsyncEngine,
):
    token, _ = token_user
    new_username = 'i_cant_contain_this -> Ъ <- symbol (and some others)'

    data, _ = await graphql_client.get_request_data(
        query=EDIT_ACCOUNT_QUERY,
        variables={
            'newUsername': new_username,
        },
        token=token,
    )
    assert data is not None
    check_validation_error(data['editAccount'], ['username'])
    assert not await try_changes(database_engine, new_username)


async def test_edit_profile_color(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    database_engine: AsyncEngine,
):
    token, user = token_user
    new_profile_color = '#c0ffee'

    data, _ = await graphql_client.get_request_data(
        query=EDIT_ACCOUNT_QUERY,
        variables={'newProfileColor': new_profile_color},
        token=token,
    )
    assert data is not None
    assert data['editAccount']['__typename'] == 'EditAccountSuccess'
    assert data['editAccount']['account']['profileColor'] == new_profile_color
    assert await try_changes(database_engine, user.username, new_profile_color)


async def test_edit_profile_color_invalid_data(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    database_engine: AsyncEngine,
):
    token, user = token_user
    new_profile_color = '#lolkek'

    data, _ = await graphql_client.get_request_data(
        query=EDIT_ACCOUNT_QUERY,
        variables={'newProfileColor': new_profile_color},
        token=token,
    )
    assert data is not None
    assert data is not None
    check_validation_error(data['editAccount'], ['profile_color'])
    assert not await try_changes(database_engine, user.username, new_profile_color)


async def test_edit_all(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    database_engine: AsyncEngine,
):
    token, _ = token_user
    new_username = '3L1T3_H4X0R_1337'
    new_profile_color = '#bad123'

    data, _ = await graphql_client.get_request_data(
        query=EDIT_ACCOUNT_QUERY,
        variables={'newUsername': new_username, 'newProfileColor': new_profile_color},
        token=token,
    )
    assert data is not None
    assert data['editAccount']['__typename'] == 'EditAccountSuccess'
    assert data['editAccount']['account']['username'] == new_username
    assert data['editAccount']['account']['profileColor'] == new_profile_color
    assert await try_changes(database_engine, new_username, new_profile_color)


async def test_edit_no_auth(
    graphql_client: GraphQLClient,
):
    new_username = '3L1T3_H4X0R_1337'
    new_profile_color = '#bad123'

    data, errors = await graphql_client.get_request_data(
        query=EDIT_ACCOUNT_QUERY,
        variables={'newUsername': new_username, 'newProfileColor': new_profile_color},
    )
    check_auth(data, errors)
