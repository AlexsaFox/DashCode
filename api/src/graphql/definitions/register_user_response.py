import strawberry

from src.graphql.definitions.user import User
from src.graphql.definitions.validation_error import ValidationError


@strawberry.type
class UserAlreadyExists:
    field: str
    value: str


@strawberry.type
class RegisterUserSuccess:
    user: User


RegisterUserResponse = strawberry.union(
    "RegisterUserResponse", (RegisterUserSuccess, UserAlreadyExists, ValidationError)
)
