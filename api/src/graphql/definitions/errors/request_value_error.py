import strawberry


@strawberry.type
class RequestValueError:
    details: str
