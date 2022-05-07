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
            user {{
                username
                email
                profileColor
            }}
        }}
    }}
}}
'''


async def test_invalid_username(graphql_client: GraphQLClient) -> None:
    response = await graphql_client.make_request(
        query=REGISTRATION_QUERY.format(
            username='i am invalid :)',
            email='valid@email.wow',
            password='longandstrongpassword',
        )
    )

    assert response.status_code == 200
    assert response.json()['data'] == None

    error_msg = response.json()['errors'][0]['message']
    assert 'Bad username' in error_msg


async def test_invalid_email(graphql_client: GraphQLClient) -> None:
    response = await graphql_client.make_request(
        query=REGISTRATION_QUERY.format(
            username='i_am_valid', email='invalid...', password='longandstrongpassword'
        )
    )

    assert response.status_code == 200
    assert response.json()['data'] == None

    error_msg = response.json()['errors'][0]['message']
    assert 'Bad email' in error_msg


async def test_invalid_password(graphql_client: GraphQLClient) -> None:
    response = await graphql_client.make_request(
        query=REGISTRATION_QUERY.format(
            username='i_am_valid', email='valid@email.wow', password='short:('
        )
    )

    assert response.status_code == 200
    assert response.json()['data'] == None

    error_msg = response.json()['errors'][0]['message']
    assert error_msg == 'Password must contain at least 8 characters'
