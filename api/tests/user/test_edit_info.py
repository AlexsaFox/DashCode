from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from src.auth.utils import AuthenticationFailedError, authenticate_user
from src.db.models import User
from tests.utils import GraphQLClient
from tests.validation.utils import check_validation_error


EDIT_USERNAME_QUERY = '''
mutation {{
    editAccount(newUsername: "{new_username}") {{
        __typename
        ... on EditAccountSuccess {{
            account {{
                user {{
                    username
                    profileColor
                }}
            }}
        }}
        ... on ValidationError {{
            fields {{
                field
                details
            }}
        }}
        ... on RequestValueError {{
            details
        }}
    }}
}}
'''
EDIT_COLOR_QUERY = '''
mutation {{
    editAccount(newProfileColor: "{new_profile_color}") {{
        __typename
        ... on EditAccountSuccess {{
            account {{
                user {{
                    username
                    profileColor
                }}
            }}
        }}
        ... on ValidationError {{
            fields {{
                field
                details
            }}
        }}
        ... on RequestValueError {{
            details
        }}
    }}
}}
'''
EDIT_ALL_QUERY = '''
mutation {{
    editAccount(newUsername: "{new_username}", newProfileColor: "{new_profile_color}") {{
        __typename
        ... on EditAccountSuccess {{
            account {{
                user {{
                    username
                    profileColor
                }}
            }}
        }}
        ... on ValidationError {{
            fields {{
                field
                details
            }}
        }}
        ... on RequestValueError {{
            details
        }}
    }}
}}
'''


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

    response = await graphql_client.make_request(
        query=EDIT_USERNAME_QUERY.format(new_username=new_username), token=token
    )
    assert response.status_code == 200

    data = response.json()['data']
    assert data['editAccount']['__typename'] == 'EditAccountSuccess'
    assert data['editAccount']['account']['user']['username'] == new_username
    assert await try_changes(database_engine, new_username)


async def test_edit_username_invalid_data(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    database_engine: AsyncEngine,
):
    token, _ = token_user
    new_username = 'i_cant_contain_this -> Ъ <- symbol (and some others)'

    response = await graphql_client.make_request(
        query=EDIT_USERNAME_QUERY.format(new_username=new_username), token=token
    )
    assert response.status_code == 200

    data = response.json()['data']
    check_validation_error(data['editAccount'], ['username'])
    assert not await try_changes(database_engine, new_username)


async def test_edit_profile_color(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    database_engine: AsyncEngine,
):
    token, user = token_user
    new_profile_color = '#c0ffee'

    response = await graphql_client.make_request(
        query=EDIT_COLOR_QUERY.format(new_profile_color=new_profile_color), token=token
    )
    assert response.status_code == 200

    data = response.json()['data']
    assert data['editAccount']['__typename'] == 'EditAccountSuccess'
    assert data['editAccount']['account']['user']['profileColor'] == new_profile_color
    assert await try_changes(database_engine, user.username, new_profile_color)


async def test_edit_profile_color_invalid_data(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    database_engine: AsyncEngine,
):
    token, user = token_user
    new_profile_color = '#lolkek'

    response = await graphql_client.make_request(
        query=EDIT_COLOR_QUERY.format(new_profile_color=new_profile_color), token=token
    )
    assert response.status_code == 200

    data = response.json()['data']
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

    response = await graphql_client.make_request(
        query=EDIT_ALL_QUERY.format(
            new_username=new_username, new_profile_color=new_profile_color
        ),
        token=token,
    )
    assert response.status_code == 200

    data = response.json()['data']
    assert data['editAccount']['__typename'] == 'EditAccountSuccess'
    assert data['editAccount']['account']['user']['username'] == new_username
    assert data['editAccount']['account']['user']['profileColor'] == new_profile_color
    assert await try_changes(database_engine, new_username, new_profile_color)
