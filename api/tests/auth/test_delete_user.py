from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import User
from tests.utils import GraphQLClient


DELETE_QUERY = '''
mutation {{
    deleteUser(password: "{password}") {{
        __typename
        ... on RequestValueError {{
            details
        }}
        ... on DeleteUserSuccess {{
            account {{
                user {{
                    username
                }}
            }}
        }}
    }}
}}
'''


async def test_delete_user(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    database_session: AsyncSession,
):
    token, user = token_user

    response = await graphql_client.make_request(
        DELETE_QUERY.format(password='password'), token=token
    )

    assert response.status_code == 200
    assert response.json() == {
        'data': {
            'deleteUser': {
                '__typename': 'DeleteUserSuccess',
                'account': {'user': {'username': user.username}},
            }
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

    response = await graphql_client.make_request(
        DELETE_QUERY.format(password='AAAAAAAAAAAAAAAAAAAAAAAA'), token=token
    )

    assert response.status_code == 200
    assert response.json() == {
        'data': {
            'deleteUser': {
                '__typename': 'RequestValueError',
                'details': 'Wrong password',
            }
        }
    }

    query = await database_session.execute(
        select(User).filter_by(username=user.username)
    )
    row = query.first()
    assert row is not None
