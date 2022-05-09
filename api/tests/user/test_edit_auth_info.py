from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from src.auth.dependencies import get_user
from src.auth.utils import AuthenticationFailedError, authenticate_user
from src.config import Configuration
from src.db.models import User
from tests.utils import GraphQLClient


EDIT_EMAIL_QUERY = '''
mutation {{
    editAccountAuth(password: "{password}", newEmail: "{new_email}") {{
        __typename
        ... on EditAccountSuccess {{
            account {{
                email
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

EDIT_PASSWORD_QUERY = '''
mutation {{
    editAccountAuth(password: "{password}", newPassword: "{new_password}") {{
        __typename
        ... on EditAccountSuccess {{
            account {{
                email
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
    editAccountAuth(password: "{password}", newEmail: "{new_email}", newPassword: "{new_password}") {{
        __typename
        ... on EditAccountSuccess {{
            account {{
                email
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


async def test_edit_email(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    database_engine: AsyncEngine,
    test_config: Configuration,
):
    token, _ = token_user
    new_email = 'different@email.com'

    response = await graphql_client.make_request(
        EDIT_EMAIL_QUERY.format(password='password', new_email=new_email),
        token=token,
    )

    assert response.status_code == 200

    data = response.json()['data']
    assert data['editAccountAuth']['__typename'] == 'EditAccountSuccess'
    assert data['editAccountAuth']['account']['email'] == new_email

    # Create new session since object is expired in old
    async with AsyncSession(database_engine) as session:
        user = await get_user(session, test_config, token)
        assert user.email == 'different@email.com'


async def test_edit_email_invalid_data(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    database_engine: AsyncEngine,
    test_config: Configuration,
):
    token, old_user = token_user
    new_email = 'he-he-he >:)'

    response = await graphql_client.make_request(
        EDIT_EMAIL_QUERY.format(password='password', new_email=new_email),
        token=token,
    )

    assert response.status_code == 200

    data = response.json()['data']
    assert data['editAccountAuth']['__typename'] == 'ValidationError'

    error_field = data['editAccountAuth']['fields'][0]
    assert error_field['field'] == 'email'
    assert error_field['details'] is not None

    # Create new session since object is expired in old
    async with AsyncSession(database_engine) as session:
        user = await get_user(session, test_config, token)
        assert user.email == old_user.email


async def test_edit_password(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    database_engine: AsyncEngine,
):
    token, old_user = token_user
    new_password = 'https://www.youtube.com/watch?v=iik25wqIuFo'

    response = await graphql_client.make_request(
        EDIT_PASSWORD_QUERY.format(password='password', new_password=new_password),
        token=token,
    )

    assert response.status_code == 200

    data = response.json()['data']
    assert data['editAccountAuth']['__typename'] == 'EditAccountSuccess'
    assert data['editAccountAuth']['account']['email'] == old_user.email

    # Create new session since object is expired in old
    async with AsyncSession(database_engine) as session:
        # This would raise error if unable to authenticate user
        # with new password. So no additional assertions are needed
        await session.run_sync(
            authenticate_user, password=new_password, email=old_user.email
        )


async def test_edit_password_invalid_data(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    database_engine: AsyncEngine,
):
    token, old_user = token_user
    new_password = 'short:('

    response = await graphql_client.make_request(
        EDIT_PASSWORD_QUERY.format(password='password', new_password=new_password),
        token=token,
    )

    assert response.status_code == 200

    data = response.json()['data']
    assert data['editAccountAuth']['__typename'] == 'ValidationError'

    error_field = data['editAccountAuth']['fields'][0]
    assert error_field['field'] == 'password'
    assert error_field['details'] is not None

    # Create new session since object is expired in old
    async with AsyncSession(database_engine) as session:
        # This would raise error if unable to authenticate user
        # with new password.
        try:
            await session.run_sync(
                authenticate_user, password=new_password, email=old_user.email
            )
        except AuthenticationFailedError:
            # So, if error is raised, then we're fine
            pass
        else:
            # But if error is not raised, then something went wrong
            raise AssertionError


async def test_edit_all(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    database_engine: AsyncEngine,
):
    token, old_user = token_user
    new_email = 'different@email.com'
    new_password = 'https://www.youtube.com/watch?v=iik25wqIuFo'

    response = await graphql_client.make_request(
        EDIT_ALL_QUERY.format(
            password='password', new_email=new_email, new_password=new_password
        ),
        token=token,
    )

    assert response.status_code == 200

    data = response.json()['data']
    assert data['editAccountAuth']['__typename'] == 'EditAccountSuccess'
    assert data['editAccountAuth']['account']['email'] == new_email

    # Create new session since object is expired in old
    async with AsyncSession(database_engine) as session:
        # This would raise error if unable to authenticate user
        # with new password. So no additional assertions are needed
        await session.run_sync(
            authenticate_user, password=new_password, email=new_email
        )
