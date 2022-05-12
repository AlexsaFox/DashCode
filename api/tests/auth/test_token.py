from typing import cast

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_user_or_none
from src.config import Configuration
from src.db.models import User
from tests.graphql.token import TOKEN_QUERY
from tests.utils import GraphQLClient


async def token_is_valid(
    token_data: dict,
    user: User,
    database_session: AsyncSession,
    config: Configuration,
):
    assert token_data['tokenType'] == 'bearer'

    user_from_token = await get_user_or_none(
        database_session, config, token_data['accessToken']
    )
    assert user_from_token is not None

    user_from_token = cast(User, user_from_token)
    assert user_from_token.username == user.username


async def test_token_by_username(
    graphql_client: GraphQLClient,
    database_session: AsyncSession,
    test_config: Configuration,
    user: User,
):
    data, _ = await graphql_client.get_request_data(
        query=TOKEN_QUERY, variables={'username': user.username, 'password': 'password'}
    )
    assert data is not None
    assert data['token']['__typename'] == 'Token'
    await token_is_valid(data['token'], user, database_session, test_config)


async def test_token_by_email(
    graphql_client: GraphQLClient,
    database_session: AsyncSession,
    test_config: Configuration,
    user: User,
):
    data, _ = await graphql_client.get_request_data(
        query=TOKEN_QUERY, variables={'email': user.email, 'password': 'password'}
    )
    assert data is not None
    assert data['token']['__typename'] == 'Token'
    await token_is_valid(data['token'], user, database_session, test_config)


async def test_login_with_bad_credentials(graphql_client: GraphQLClient, user: User):

    data, _ = await graphql_client.get_request_data(
        query=TOKEN_QUERY,
        variables={'username': 'wrong' + user.username, 'password': 'password'},
    )
    assert data is not None
    assert data['token']['__typename'] == 'RequestValueError'
    assert data['token']['details'] is not None
