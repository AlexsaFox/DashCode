import strawberry

from src.db.models import User as UserModel


@strawberry.type
class User:
    username: str
    profile_color: str
    is_superuser: bool
    profile_picture_filename: str

    @classmethod
    def from_instance(cls, instance: UserModel):
        return cls(
            username=instance.username,
            profile_color=instance.profile_color,
            is_superuser=instance.is_superuser,
            profile_picture_filename=instance.profile_picture_filename,
        )


@strawberry.type
class Account:
    user: User
    email: str

    @classmethod
    def from_instance(cls, instance: UserModel):
        return cls(
            user=User.from_instance(instance),
            email=instance.email,
        )
