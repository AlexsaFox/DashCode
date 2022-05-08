from src.db.models import User
from tests.utils import GraphQLClient


WHOAMI_QUERY = '''
{
    whoami {
        user {
            username
            profileColor
            isSuperuser
        }
        email
    }
}
'''


async def test_whoami(graphql_client: GraphQLClient, token_user: tuple[str, User]):
    token, user = token_user

    response = await graphql_client.make_request(WHOAMI_QUERY, token=token)

    assert response.status_code == 200
    assert response.json().get('errors') is None

    user_data = response.json()['data']['whoami']
    assert user_data['email'] == user.email
    assert user_data['user']['username'] == user.username
    assert user_data['user']['profileColor'] == user.profile_color
    assert user_data['user']['isSuperuser'] == user.is_superuser
