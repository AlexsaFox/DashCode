from src.db.models import User
from tests.graphql.get_user import USER_GET_QUERY
from tests.utils import GraphQLClient


async def test_user_receiving(
    graphql_client: GraphQLClient, token_user: tuple[str, User]
):
    token, user = token_user
    data, _ = await graphql_client.get_request_data(
        query=USER_GET_QUERY,
        variables={"username": user.username},
        token=token,
    )
    assert data is not None
    assert data['getUser']['__typename'] == "GetUserSuccess"
    assert data == {
        "getUser": {"__typename": "GetUserSuccess", "user": {"username": user.username}}
    }


async def test_user_receiving_invalid_username(
    graphql_client: GraphQLClient, token_user: tuple[str, User]
):
    token, _ = token_user
    data, _ = await graphql_client.get_request_data(
        query=USER_GET_QUERY,
        variables={"username": "blabla"},
        token=token,
    )
    assert data is not None
    assert data['getUser']['__typename'] == "RequestValueError"
    assert data == {
        "getUser": {
            "__typename": "RequestValueError",
            "details": "Unable to find a user with provided username",
        }
    }


async def test_user_receiving_no_auth(graphql_client: GraphQLClient):
    _, errors = await graphql_client.get_request_data(
        query=USER_GET_QUERY,
        variables={"username": "blabla"},
    )
    assert errors is not None
    assert errors[0]['message'] == 'Authentication required'
