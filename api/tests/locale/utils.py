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


async def check_localization(
    graphql_client: GraphQLClient, user: User, lang_header: str, correct_err_str: str
):
    response = await graphql_client.make_request(
        TOKEN_QUERY_USERNAME.format(
            username=user.username, password='T0tallyWrongPa$$w0rD!!!'
        ),
        lang_header=lang_header,
    )

    assert response.status_code == 200

    data = response.json()['data']['token']
    assert data['__typename'] == 'RequestValueError'
    assert data['details'] == correct_err_str
