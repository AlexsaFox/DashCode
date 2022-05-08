import strawberry

from src.graphql.definitions.errors.wrong_password import WrongPasswordError
from src.graphql.definitions.user import Account


@strawberry.type
class DeleteUserSuccess:
    account: Account


DeleteUserResponse = strawberry.union(
    'DeleteUserResponse', (DeleteUserSuccess, WrongPasswordError)
)
