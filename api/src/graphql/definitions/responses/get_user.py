import strawberry

from src.graphql.definitions.errors.request_value_error import RequestValueError
from src.graphql.definitions.user import User


@strawberry.type
class GetUserSuccess:
    user: User


GetUserResponse = strawberry.union(
    "GetUserResponse", (GetUserSuccess, RequestValueError)
)
