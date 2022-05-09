import strawberry

from src.db.models import User as UserModel


@strawberry.type
class User:
    username: str
    email: str
    profile_color: str
    is_superuser: bool

    @classmethod
    def from_instance(cls, instance: UserModel):
        return cls(
            username=instance.username,
            email=instance.email,
            profile_color=instance.profile_color,
            is_superuser=instance.is_superuser,
        )
