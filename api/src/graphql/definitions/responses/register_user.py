import strawberry

from src.graphql.definitions.errors.validation_error import ValidationError
from src.graphql.definitions.user import Account


@strawberry.type
class UserAlreadyExists:
    field: str
    value: str


@strawberry.type
class RegisterUserSuccess:
    account: Account


RegisterUserResponse = strawberry.union(
    "RegisterUserResponse", (RegisterUserSuccess, UserAlreadyExists, ValidationError)
)
