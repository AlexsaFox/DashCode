from typing import cast

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_user_or_none
from src.config import Configuration
from src.db.models import User
from tests.utils import GraphQLClient


TOKEN_QUERY_USERNAME = '''
{{
    token(username: "{username}", password: "{password}") {{
        __typename
        ... on RequestValueError {{
            details
        }}
        ... on Token {{
            accessToken
            tokenType
        }}
    }}
}}
'''
TOKEN_QUERY_EMAIL = '''
{{
    token(email: "{email}", password: "{password}") {{
        __typename
        ... on RequestValueError {{
            details
        }}
        ... on Token {{
            accessToken
            tokenType
        }}
    }}
}}
'''


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
    response = await graphql_client.make_request(
        TOKEN_QUERY_USERNAME.format(username=user.username, password='password')
    )
    assert response.status_code == 200
    assert response.json().get('errors') is None

    data = response.json()['data']
    assert data['token']['__typename'] == 'Token'
    await token_is_valid(data['token'], user, database_session, test_config)


async def test_token_by_email(
    graphql_client: GraphQLClient,
    database_session: AsyncSession,
    test_config: Configuration,
    user: User,
):
    response = await graphql_client.make_request(
        TOKEN_QUERY_EMAIL.format(email=user.email, password='password')
    )
    assert response.status_code == 200
    assert response.json().get('errors') is None

    data = response.json()['data']
    assert data['token']['__typename'] == 'Token'
    await token_is_valid(data['token'], user, database_session, test_config)


async def test_login_with_bad_creds(graphql_client: GraphQLClient, user: User):
    response = await graphql_client.make_request(
        TOKEN_QUERY_USERNAME.format(
            username='wrong' + user.username, password='password'
        )
    )
    assert response.status_code == 200

    data = response.json()['data']
    assert data['token']['__typename'] == 'RequestValueError'
    assert data['token']['details'] is not None
