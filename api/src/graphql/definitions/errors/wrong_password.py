import strawberry

from src.graphql.definitions.errors.response_error import ResponseError


@strawberry.type
class WrongPasswordError(ResponseError):
    pass
