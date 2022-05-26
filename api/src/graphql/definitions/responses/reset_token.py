import strawberry

from src.graphql.definitions.errors.request_value_error import RequestValueError
from src.graphql.definitions.token import Token


@strawberry.type
class ResetTokenSuccess:
    token: Token


ResetTokenResponse = strawberry.union(
    'ResetTokenResponse', (ResetTokenSuccess, RequestValueError)
)
