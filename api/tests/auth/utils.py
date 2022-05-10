from typing import Any

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from src.auth.utils import AuthenticationFailedError, authenticate_user


async def try_credentials(engine: AsyncEngine, email: str, password: str) -> bool:
    try:
        async with AsyncSession(engine) as session:
            await session.run_sync(authenticate_user, password=password, email=email)
        return True
    except AuthenticationFailedError:
        return False


def check_auth(data: dict[str, Any] | None, errors: list[dict[str, Any]] | None):
    assert data is None
    assert errors is not None
    assert errors[0]['message'] == 'Authentication required'
