import os

from aiofile import async_open
from fastapi import APIRouter, Depends, HTTPException, Response

from src.config import BASE_DIR, Configuration
from src.dependencies import get_config
from src.utils.file_upload import get_image_mime_type


router = APIRouter()


@router.get('/ping')
async def ping() -> str:
    return 'pong'


@router.get('/uploads/{filename}')
async def serve_uploads(
    filename: str, config: Configuration = Depends(get_config)
) -> Response | HTTPException:
    try:
        full_path = os.path.join(BASE_DIR, config.file_upload.upload_path, filename)
        async with async_open(full_path, 'rb') as af:
            data = await af.read()
        _, _, extension = filename.rpartition('.')
        return Response(data, media_type=get_image_mime_type(extension))
    except FileNotFoundError:
        return HTTPException(status_code=404)
