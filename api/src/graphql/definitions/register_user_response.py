import strawberry

from src.graphql.definitions.user import Account
from src.graphql.definitions.validation_error import ValidationError


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
