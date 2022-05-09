import os

from aiofile import async_open
from fastapi import APIRouter, HTTPException, Response

from src.config import BASE_DIR


router = APIRouter()


@router.get('/ping')
async def ping() -> str:
    return 'pong'


@router.get('/uploads/{filename}')
async def serve_uploads(filename: str) -> Response | HTTPException:
    try:
        full_path = os.path.join(BASE_DIR, 'uploads', filename)
        async with async_open(full_path, 'rb') as af:
            data = await af.read()
        _, _, extension = filename.rpartition('.')
        return Response(data, media_type=f'image/{extension}')
    except FileNotFoundError:
        return HTTPException(status_code=404)
