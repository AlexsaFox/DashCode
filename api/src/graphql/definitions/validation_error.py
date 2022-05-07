import strawberry


@strawberry.type
class FieldError:
    field: str
    details: str


@strawberry.type
class ValidationError:
    fields: list[FieldError]
