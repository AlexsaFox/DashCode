from fastapi import Request

from src.config import Configuration
from src.types import AppState


async def get_config(request: Request) -> Configuration:
    app_state: AppState = request.app.app_state
    return app_state.config
