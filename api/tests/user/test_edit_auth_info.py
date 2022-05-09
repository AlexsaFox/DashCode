from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from src.auth.dependencies import get_user
from src.auth.utils import AuthenticationFailedError, authenticate_user
from src.config import Configuration
from src.db.models import User
from tests.utils import GraphQLClient
from tests.validation.utils import check_validation_error


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


async def try_credentials(engine: AsyncEngine, email: str, password: str) -> bool:
    try:
        async with AsyncSession(engine) as session:
            await session.run_sync(authenticate_user, password=password, email=email)
        return True
    except AuthenticationFailedError:
        return False


async def test_edit_email(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    database_engine: AsyncEngine,
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

    assert await try_credentials(database_engine, new_email, 'password')


async def test_edit_email_invalid_data(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    database_engine: AsyncEngine,
):
    token, _ = token_user
    new_email = 'he-he-he >:)'

    response = await graphql_client.make_request(
        EDIT_EMAIL_QUERY.format(password='password', new_email=new_email),
        token=token,
    )
    assert response.status_code == 200

    data = response.json()['data']
    check_validation_error(data['editAccountAuth'], ['email'])
    assert not await try_credentials(database_engine, new_email, 'password')


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

    assert await try_credentials(database_engine, old_user.email, new_password)


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

    assert await try_credentials(database_engine, new_email, new_password)


async def test_edit_bad_password(
    graphql_client: GraphQLClient,
    token_user: tuple[str, User],
    database_engine: AsyncEngine,
):
    token, _ = token_user
    new_email = 'different@email.com'

    response = await graphql_client.make_request(
        EDIT_EMAIL_QUERY.format(
            password='never gonna give you up', new_email=new_email
        ),
        token=token,
    )
    assert response.status_code == 200

    data = response.json()['data']
    assert data['editAccountAuth']['__typename'] == 'RequestValueError'
    assert data['editAccountAuth']['details'] == 'Wrong password'

    assert not await try_credentials(database_engine, new_email, 'password')
