from src.db.models import User
from tests.utils import GraphQLClient
from tests.validation.utils import check_validation_error


REGISTRATION_QUERY = '''
mutation {{
    registerUser(username: "{username}", email: "{email}", password: "{password}") {{
        __typename
        ... on UserAlreadyExists {{
            field
            value
        }}
        ... on RegisterUserSuccess {{
            account {{
                user {{
                    username
                    profileColor
                    isSuperuser
                }}
                email
            }}
        }}
        ... on ValidationError {{
            fields {{
                field
                details
            }}
        }}
    }}
}}
'''


async def test_registration(graphql_client: GraphQLClient) -> None:
    response = await graphql_client.make_request(
        query=REGISTRATION_QUERY.format(
            username='user', email='user@user.com', password='longandstrongpassword'
        )
    )

    assert response.status_code == 200
    assert response.json() == {
        'data': {
            'registerUser': {
                '__typename': 'RegisterUserSuccess',
                'account': {
                    'user': {
                        'username': 'user',
                        'profileColor': '#ffffff',
                        'isSuperuser': False,
                    },
                    'email': 'user@user.com',
                },
            }
        }
    }


async def test_registration_duplicate_username(
    graphql_client: GraphQLClient, user: User
) -> None:
    response = await graphql_client.make_request(
        query=REGISTRATION_QUERY.format(
            username=user.username,
            email='unique' + user.email,
            password='longandstrongpassword',
        )
    )

    assert response.status_code == 200
    assert response.json() == {
        'data': {
            'registerUser': {
                '__typename': 'UserAlreadyExists',
                'field': 'username',
                'value': user.username,
            }
        }
    }


async def test_registration_duplicate_email(
    graphql_client: GraphQLClient, user: User
) -> None:
    response = await graphql_client.make_request(
        query=REGISTRATION_QUERY.format(
            username='unique' + user.username,
            email=user.email,
            password='longandstrongpassword',
        )
    )

    assert response.status_code == 200
    assert response.json() == {
        'data': {
            'registerUser': {
                '__typename': 'UserAlreadyExists',
                'field': 'email',
                'value': user.email,
            }
        }
    }


async def test_registration_invalid_username(graphql_client: GraphQLClient) -> None:
    response = await graphql_client.make_request(
        query=REGISTRATION_QUERY.format(
            username='i am invalid :)',
            email='valid@email.wow',
            password='longandstrongpassword',
        )
    )
    assert response.status_code == 200

    data = response.json()['data']
    check_validation_error(data['registerUser'], ['username'])


async def test_registration_invalid_email(graphql_client: GraphQLClient) -> None:
    response = await graphql_client.make_request(
        query=REGISTRATION_QUERY.format(
            username='i_am_valid', email='invalid...', password='longandstrongpassword'
        )
    )
    assert response.status_code == 200

    data = response.json()['data']
    check_validation_error(data['registerUser'], ['email'])


async def test_registration_invalid_password(graphql_client: GraphQLClient) -> None:
    response = await graphql_client.make_request(
        query=REGISTRATION_QUERY.format(
            username='i_am_valid', email='valid@email.wow', password='short:('
        )
    )
    assert response.status_code == 200

    data = response.json()['data']
    check_validation_error(data['registerUser'], ['password'])


async def test_registration_multiple_bad(graphql_client: GraphQLClient) -> None:
    response = await graphql_client.make_request(
        query=REGISTRATION_QUERY.format(
            username='i am invalid :)',
            email='invalid...',
            password='short:(',
        )
    )
    assert response.status_code == 200

    data = response.json()['data']
    check_validation_error(data['registerUser'], ['username', 'email', 'password'])
