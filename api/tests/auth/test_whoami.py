from src.db.models import User
from tests.auth.utils import check_auth
from tests.graphql.whoami import WHOAMI_QUERY
from tests.utils import GraphQLClient


async def test_whoami(graphql_client: GraphQLClient, token_user: tuple[str, User]):
    token, user = token_user

    data, _ = await graphql_client.get_request_data(query=WHOAMI_QUERY, token=token)
    assert data is not None
    user_data = data['whoami']
    assert user_data['email'] == user.email
    assert user_data['user']['username'] == user.username
    assert user_data['user']['profileColor'] == user.profile_color
    assert user_data['user']['isSuperuser'] == user.is_superuser


async def test_whoami_no_auth(graphql_client: GraphQLClient):
    data, errors = await graphql_client.get_request_data(query=WHOAMI_QUERY)
    check_auth(data, errors)
