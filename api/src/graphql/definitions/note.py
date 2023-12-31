from datetime import datetime

import strawberry

from src.db.models import Note as NoteModel
from src.graphql.definitions.pagination import Cursor, Edge


# Following import was moved to bottom of file to resolve circular import issue
# from src.graphql.definitions.user import User


@strawberry.type
class Note:
    id: str
    title: str
    content: str
    link: str
    is_private: bool
    tags: list[str]
    creation_date: datetime
    user: 'User'

    @classmethod
    def from_instance(cls, instance: NoteModel):
        return cls(
            id=instance.id,
            title=instance.title,
            content=instance.content,
            link=instance.link,
            is_private=instance.is_private,
            creation_date=instance.creation_date,
            user=User.from_instance(instance.user),
            tags=[tag.content for tag in instance.tags],
        )

    @classmethod
    def from_instance_and_user(cls, instance: NoteModel, user: 'User'):
        return cls(
            id=instance.id,
            title=instance.title,
            content=instance.content,
            link=instance.link,
            is_private=instance.is_private,
            creation_date=instance.creation_date,
            user=user,
            tags=[tag.content for tag in instance.tags],
        )

    def get_cursor(self) -> Cursor:
        return self.id

    def id_from_cursor(self, cursor: Cursor):
        return cursor

    def to_edge(self) -> Edge['Note']:
        return Edge(node=self, cursor=self.get_cursor())


from src.graphql.definitions.user import User
