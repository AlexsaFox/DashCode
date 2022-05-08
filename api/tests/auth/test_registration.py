from src.db.models import User
from tests.utils import GraphQLClient


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


async def test_invalid_value(graphql_client: GraphQLClient) -> None:
    response = await graphql_client.make_request(
        query=REGISTRATION_QUERY.format(
            username='this is definitely not a valid username because it has spaces',
            email='valid@email.wow',
            password='longandstrongpassword',
        )
    )

    assert response.status_code == 200
    assert response.json()['data']['registerUser']['__typename'] == 'ValidationError'
