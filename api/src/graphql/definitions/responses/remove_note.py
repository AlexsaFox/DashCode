import strawberry

from src.graphql.definitions.errors.request_value_error import RequestValueError
from src.graphql.definitions.note import Note


@strawberry.type
class RemoveNoteSuccess:
    note: Note


RemoveNoteResponse = strawberry.union(
    'RemoveNoteResponse', (RemoveNoteSuccess, RequestValueError)
)
