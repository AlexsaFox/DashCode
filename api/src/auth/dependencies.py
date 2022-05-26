from authlib.jose.errors import (
    BadSignatureError,
    DecodeError,
    ExpiredTokenError,
    InvalidClaimError,
)
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.engine.row import Row
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.auth.utils import decode_jwt
from src.config import Configuration
from src.db.dependencies import get_session
from src.db.models import User
from src.dependencies import get_config


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token', auto_error=False)


async def get_user_or_none(
    session: AsyncSession = Depends(get_session),
    config: Configuration = Depends(get_config),
    token: str | None = Depends(oauth2_scheme),
) -> User | None:
    if token is None:
        return None

    try:
        jwt_claims = decode_jwt(config, token)
    except (BadSignatureError, DecodeError, ExpiredTokenError, InvalidClaimError):
        return None

    user_id = int(jwt_claims['sub'])
    user_proof = jwt_claims.get('proof')
    query = await session.execute(select(User).filter_by(id=user_id))
    row: Row | None = query.one_or_none()
    if row is None:
        return None
    user: User = row[0]

    if user.jwt_proof != user_proof:
        return None

    return user


async def get_user(
    session: AsyncSession = Depends(get_session),
    config: Configuration = Depends(get_config),
    token: str | None = Depends(oauth2_scheme),
) -> User:
    authentication_failed = HTTPException(
        status_code=401,
        detail='Authentication required',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    user: User | None = await get_user_or_none(session, config, token)
    if user is None:
        raise authentication_failed
    return user
