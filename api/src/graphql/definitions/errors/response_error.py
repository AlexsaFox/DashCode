import strawberry


@strawberry.type
class ResponseError:
    details: str
