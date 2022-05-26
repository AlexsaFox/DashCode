from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from src.config import Configuration
from src.db.models import User
from tests.auth.test_token import token_is_valid
from tests.auth.utils import check_auth_error
from tests.graphql.reset_token import RESET_TOKEN_QUERY
from tests.utils import GraphQLClient


async def test_reset_token(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    database_engine: AsyncEngine,
    test_config: Configuration,
):
    token, user = token_user

    data, _ = await graphql_client.get_request_data(
        query=RESET_TOKEN_QUERY, variables={'password': 'password'}, token=token
    )
    assert data is not None
    assert data['resetToken']['__typename'] == 'ResetTokenSuccess'

    token_data = data['resetToken']['token']

    async with AsyncSession(database_engine) as session:
        assert await token_is_valid(token_data, user, session, test_config)
        assert not await token_is_valid(
            {'tokenType': 'bearer', 'accessToken': token},
            user,
            session,
            test_config,
        )


async def test_reset_token_wrong_password(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    database_engine: AsyncEngine,
    test_config: Configuration,
):
    token, user = token_user

    data, _ = await graphql_client.get_request_data(
        query=RESET_TOKEN_QUERY,
        variables={'password': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAA'},
        token=token,
    )

    assert data is not None
    assert data == {
        'resetToken': {
            '__typename': 'RequestValueError',
            'details': 'Wrong password',
        }
    }
    async with AsyncSession(database_engine) as session:
        assert await token_is_valid(
            {'tokenType': 'bearer', 'accessToken': token},
            user,
            session,
            test_config,
        )


async def test_reset_token_no_auth(graphql_client: GraphQLClient):
    data, errors = await graphql_client.get_request_data(
        query=RESET_TOKEN_QUERY,
        variables={'password': 'password'},
    )
    check_auth_error(data, errors)
