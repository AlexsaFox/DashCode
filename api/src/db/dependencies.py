from typing import AsyncGenerator

from fastapi import Request
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.types import AppState


async def get_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    app_state: AppState = request.app.app_state

    async with AsyncSession(app_state.engine) as session:
        yield session
