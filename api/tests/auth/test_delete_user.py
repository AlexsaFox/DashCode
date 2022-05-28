from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import User
from tests.auth.utils import check_auth_error
from tests.graphql.delete_user import DELETE_USER_QUERY
from tests.utils import GraphQLClient


async def user_exists(session: AsyncSession, username: str) -> bool:
    query = await session.execute(select(User).filter_by(username=username))
    row = query.first()
    return row is not None


async def test_delete_user(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    database_session: AsyncSession,
):
    token, user = token_user

    data, _ = await graphql_client.get_request_data(
        query=DELETE_USER_QUERY, variables={'password': 'password'}, token=token
    )
    assert data is not None
    assert data == {
        'deleteUser': {
            '__typename': 'DeleteUserSuccess',
            'account': {'username': user.username},
        }
    }
    assert not await user_exists(database_session, user.username)


async def test_delete_user_wrong_password(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    database_session: AsyncSession,
):
    token, user = token_user

    data, _ = await graphql_client.get_request_data(
        query=DELETE_USER_QUERY,
        variables={'password': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAA'},
        token=token,
    )

    assert data is not None
    assert data == {
        'deleteUser': {
            '__typename': 'RequestValueError',
            'details': 'Wrong password',
        }
    }
    assert await user_exists(database_session, user.username)


async def test_delete_user_no_auth(graphql_client: GraphQLClient):
    data, errors = await graphql_client.get_request_data(
        query=DELETE_USER_QUERY,
        variables={'password': 'password'},
    )
    check_auth_error(data, errors)
