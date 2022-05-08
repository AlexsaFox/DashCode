import strawberry

from src.graphql.definitions.errors.request_value_error import RequestValueError


@strawberry.type
class FieldError(RequestValueError):
    field: str


@strawberry.type
class ValidationError:
    fields: list[FieldError]
