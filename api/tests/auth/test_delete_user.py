from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import User
from tests.graphql.delete_user import DELETE_USER_QUERY
from tests.utils import GraphQLClient


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
            'account': {'user': {'username': user.username}},
        }
    }

    query = await database_session.execute(
        select(User).filter_by(username=user.username)
    )
    row = query.first()
    assert row is None


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

    query = await database_session.execute(
        select(User).filter_by(username=user.username)
    )
    row = query.first()
    assert row is not None
