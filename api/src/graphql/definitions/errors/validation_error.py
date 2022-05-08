import strawberry

from src.graphql.definitions.errors.response_error import ResponseError


@strawberry.type
class FieldError(ResponseError):
    field: str


@strawberry.type
class ValidationError:
    fields: list[FieldError]
