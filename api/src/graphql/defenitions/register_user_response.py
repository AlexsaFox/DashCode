import strawberry

from src.graphql.defenitions.user import User


@strawberry.type
class UserAlreadyExists:
    field: str
    value: str


@strawberry.type
class RegisterUserSuccess:
    user: User


RegisterUserResponse = strawberry.union(
    "RegisterUserResponse", (RegisterUserSuccess, UserAlreadyExists)
)
