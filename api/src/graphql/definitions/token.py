import strawberry

from strawberry.types import Info
from src.auth.utils import generate_jwt

from src.config import Configuration
from src.db.models import User as UserModel


@strawberry.type
class Token:
    access_token: str
    token_type: str = 'bearer'

    @classmethod
    def from_user(cls, user: UserModel, info: Info):
        config: Configuration = info.context['config']
        token = generate_jwt(config, user)
        return cls(access_token=token)
