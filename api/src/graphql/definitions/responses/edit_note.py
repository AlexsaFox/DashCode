import strawberry

from src.graphql.definitions.errors.request_value_error import RequestValueError
from src.graphql.definitions.errors.validation_error import ValidationError
from src.graphql.definitions.note import Note


@strawberry.type
class EditNoteSuccess:
    note: Note


EditNoteResponse = strawberry.union(
    'EditNoteResponse', (EditNoteSuccess, ValidationError, RequestValueError)
)
