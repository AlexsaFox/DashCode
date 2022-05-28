import strawberry

from src.graphql.definitions.errors.request_value_error import RequestValueError
from src.graphql.definitions.token import Token


GetTokenResponse = strawberry.union('GetTokenResponse', (Token, RequestValueError))
