import strawberry

from src.graphql.definitions.errors.request_value_error import RequestValueError
from src.graphql.definitions.errors.validation_error import ValidationError
from src.graphql.definitions.user import Account


@strawberry.type
class EditAccountSuccess:
    account: Account


EditAccountAuthResponse = strawberry.union(
    'EditAccountResponse', (EditAccountSuccess, RequestValueError, ValidationError)
)

EditAccountResponse = strawberry.union(
    'EditAccountResponse', (EditAccountSuccess, ValidationError)
)
