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


async def test_invalid_username(graphql_client: GraphQLClient) -> None:
    response = await graphql_client.make_request(
        query=REGISTRATION_QUERY.format(
            username='i am invalid :)',
            email='valid@email.wow',
            password='longandstrongpassword',
        )
    )

    assert response.status_code == 200

    data = response.json()['data']['registerUser']
    assert data['__typename'] == 'ValidationError'

    error_data = data['fields'][0]
    assert error_data['field'] == 'username'
    assert 'username' in error_data['details'].lower()


async def test_invalid_email(graphql_client: GraphQLClient) -> None:
    response = await graphql_client.make_request(
        query=REGISTRATION_QUERY.format(
            username='i_am_valid', email='invalid...', password='longandstrongpassword'
        )
    )

    assert response.status_code == 200

    data = response.json()['data']['registerUser']
    assert data['__typename'] == 'ValidationError'

    error_data = data['fields'][0]
    assert error_data['field'] == 'email'
    assert 'email' in error_data['details'].lower()


async def test_invalid_password(graphql_client: GraphQLClient) -> None:
    response = await graphql_client.make_request(
        query=REGISTRATION_QUERY.format(
            username='i_am_valid', email='valid@email.wow', password='short:('
        )
    )

    assert response.status_code == 200

    data = response.json()['data']['registerUser']
    assert data['__typename'] == 'ValidationError'

    error_data = data['fields'][0]
    assert error_data['field'] == 'password'
    assert 'password' in error_data['details'].lower()


async def test_multiple_bad(graphql_client: GraphQLClient) -> None:
    response = await graphql_client.make_request(
        query=REGISTRATION_QUERY.format(
            username='i am invalid :)',
            email='invalid...',
            password='short:(',
        )
    )

    assert response.status_code == 200

    data = response.json()['data']['registerUser']
    assert data['__typename'] == 'ValidationError'
    assert len(data['fields']) == 3

    error_field_names = [field['field'] for field in data['fields']]
    assert 'username' in error_field_names
    assert 'email' in error_field_names
    assert 'password' in error_field_names
