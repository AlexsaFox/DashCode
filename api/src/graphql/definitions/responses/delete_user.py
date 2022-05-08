import strawberry

from src.graphql.definitions.errors.request_value_error import RequestValueError
from src.graphql.definitions.user import Account


@strawberry.type
class DeleteUserSuccess:
    account: Account


DeleteUserResponse = strawberry.union(
    'DeleteUserResponse', (DeleteUserSuccess, RequestValueError)
)
