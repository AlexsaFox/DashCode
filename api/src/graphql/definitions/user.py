import strawberry

from src.db.models import User as UserModel


# Following import was moved to bottom of file to resolve circular import issue
# from src.graphql.definitions.note import Note


@strawberry.type
class User:
    username: str
    profile_color: str
    is_superuser: bool
    profile_picture_filename: str | None
    notes: list['Note']

    @classmethod
    def from_instance(cls, instance: UserModel):
        user = cls(
            username=instance.username,
            profile_color=instance.profile_color,
            is_superuser=instance.is_superuser,
            profile_picture_filename=instance.profile_picture_filename,
            notes=[],
        )
        user.notes = [
            Note.from_instance_and_user(note, user)
            for note in instance.notes
            if not note.is_private
        ]
        return user


@strawberry.type
class Account(User):
    email: str

    @classmethod
    def from_instance(cls, instance: UserModel):
        user = cls(
            username=instance.username,
            email=instance.email,
            profile_color=instance.profile_color,
            is_superuser=instance.is_superuser,
            profile_picture_filename=instance.profile_picture_filename,
            notes=[],
        )
        user.notes = [
            Note.from_instance_and_user(note, user) for note in instance.notes
        ]
        return user


from src.graphql.definitions.note import Note
