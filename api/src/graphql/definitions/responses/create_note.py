import strawberry

from src.graphql.definitions.errors.validation_error import ValidationError
from src.graphql.definitions.note import Note


@strawberry.type
class CreateNoteSuccess:
    note: Note


CreateNoteResponse = strawberry.union(
    'CreateNoteResponse', (CreateNoteSuccess, ValidationError)
)
