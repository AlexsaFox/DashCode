import strawberry

from src.db.errors import ObjectExistsError
from src.graphql.definitions.errors.validation_error import ValidationError
from src.graphql.definitions.user import Account


@strawberry.type
class UserAlreadyExists:
    field: str
    value: str

    @classmethod
    def from_exception(cls, err: ObjectExistsError):
        return cls(field=err.field, value=err.value)


@strawberry.type
class RegisterUserSuccess:
    account: Account


RegisterUserResponse = strawberry.union(
    "RegisterUserResponse", (RegisterUserSuccess, UserAlreadyExists, ValidationError)
)
