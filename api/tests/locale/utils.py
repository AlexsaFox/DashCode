from src.db.models import User
from tests.graphql.token import TOKEN_QUERY
from tests.utils import GraphQLClient


async def check_localization(
    graphql_client: GraphQLClient, user: User, lang_header: str, correct_err_str: str
):
    data, _ = await graphql_client.get_request_data(
        query=TOKEN_QUERY,
        variables={'username': user.username, 'password': 'T0tallyWrongPa$$w0rD!!!'},
        lang_header=lang_header,
    )
    assert data is not None
    assert data['token']['__typename'] == 'RequestValueError'
    assert data['token']['details'] == correct_err_str
