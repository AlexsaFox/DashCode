from typing import cast

from sqlalchemy import select
from sqlalchemy.engine.row import Row
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.utils import authenticate_user
from src.create_app import App
from src.db.models import User
from src.config import Configuration


async def test_default_superuser(
    test_config: Configuration, database_session: AsyncSession, app: App
):
    base_superuser = test_config.base_superuser

    # Check that user exists
    query = await database_session.execute(
        select(User).filter_by(username=base_superuser.username)
    )
    row: Row | None = query.first()
    assert row is not None

    # Check basic info
    user: User = cast(Row, row)[0]
    assert user.username == base_superuser.username
    assert user.email == base_superuser.email

    # Check password
    authenticated_user = await database_session.run_sync(
        authenticate_user, username=user.username, password=base_superuser.password
    )
    assert authenticated_user.id == user.id
