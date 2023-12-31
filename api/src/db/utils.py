import os
from base64 import urlsafe_b64encode
from secrets import token_bytes

from aiofile import async_open
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from src.config import BASE_DIR, DatabaseConfiguration, FileUploadConfiguration
from src.db.validation import validate_file


def get_engine(config: DatabaseConfiguration) -> AsyncEngine:
    return create_async_engine(config.dsn)


def ensure_path_exists(path: str):
    if not os.path.exists(path):
        os.makedirs(path)


async def save_file(config: FileUploadConfiguration, file: UploadFile) -> str:
    validate_file(config, file)
    _, _, extension = file.filename.rpartition('.')
    filename = urlsafe_b64encode(token_bytes(24)).decode() + '.' + extension
    folder_path = os.path.join(BASE_DIR, config.upload_path)
    full_path = os.path.join(folder_path, filename)

    ensure_path_exists(folder_path)
    async with async_open(full_path, 'wb') as af:
        await af.write(await file.read())
    return filename


def delete_file(config: FileUploadConfiguration, filename: str):
    full_path = os.path.join(BASE_DIR, config.upload_path, filename)
    os.remove(full_path)
