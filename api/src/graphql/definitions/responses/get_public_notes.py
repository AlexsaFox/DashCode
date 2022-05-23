import strawberry

from src.graphql.definitions.errors.request_value_error import RequestValueError
from src.graphql.definitions.note import Note
from src.graphql.definitions.pagination import Connection


GetPublicNotesResponse = strawberry.union(
    "GetPublicNoteResponse", (Connection[Note], RequestValueError)
)
