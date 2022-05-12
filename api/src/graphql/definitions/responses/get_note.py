import strawberry

from src.graphql.definitions.errors.request_value_error import RequestValueError
from src.graphql.definitions.note import Note


@strawberry.type
class GetNoteSuccess:
    note: Note


GetNoteResponse = strawberry.union(
    "GetNoteResponse", (GetNoteSuccess, RequestValueError)
)
