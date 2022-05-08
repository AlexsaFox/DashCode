import strawberry

from src.db.validation import ModelFieldValidationError
from src.graphql.definitions.errors.request_value_error import RequestValueError
from src.locale.dependencies import Translator


@strawberry.type
class FieldError(RequestValueError):
    field: str


@strawberry.type
class ValidationError:
    fields: list[FieldError]

    @classmethod
    def from_exception(cls, exception: ModelFieldValidationError, t: Translator):
        model = exception.model_name
        error_fields = [
            FieldError(field=field, details=t(f'validation.errors.{model}.{field}'))
            for field in exception.fields
        ]
        return cls(error_fields)
