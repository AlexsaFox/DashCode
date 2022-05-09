import strawberry

from src.graphql.definitions.errors.validation_error import ValidationError
from src.graphql.definitions.note import Note


CreateNoteResponse = strawberry.union('CreateNoteResponse', (Note, ValidationError))
