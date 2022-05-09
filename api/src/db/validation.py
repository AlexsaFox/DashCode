import re

from fastapi import UploadFile

from src.config import FileUploadConfiguration
from src.types import ExpectedError


EMAIL_REGEXP = re.compile(r'(?=.{1,120}$)[^@]+@[^@]+\.[^@]+')
USERNAME_REGEXP = re.compile(r'[a-zA-Z0-9_\-\.]{1,80}')
PASSWORD_REGEXP = re.compile(r'.{8,}')
COLOR_REGEXP = re.compile(r'#[a-fA-F0-9]{6}')


class ModelFieldValidationError(ExpectedError):
    def __init__(self, model: object, fields: list[str]):
        self.fields = fields
        self.model_name = type(model).__name__.lower()
        super().__init__(
            f'validation for following fields of model {self.model_name} has failed:'
            f' {", ".join(fields)}'
        )


def validate_file(config: FileUploadConfiguration, file: UploadFile):
    mime_type = file.content_type
    if not mime_type.startswith('image/'):
        raise FileBadMimeTypeError()

    filename = file.filename
    _, _, extension = filename.rpartition('.')
    if extension not in config.allowed_extensions:
        raise FileBadExtensionError()

    file_sync = file.file
    file_sync.seek(0, 2)
    size = file_sync.tell()
    file_sync.seek(0)
    if size / (2 << 20) > config.max_size_mb:
        raise FileTooLargeError()


class FileBadMimeTypeError(ValueError):
    def __init__(self, msg: str = 'Uploaded file extension is not supported'):
        super().__init__(msg)


class FileBadExtensionError(ValueError):
    def __init__(self, msg: str = 'Uploaded file extension is not supported'):
        super().__init__(msg)


class FileTooLargeError(ValueError):
    def __init__(self, msg: str = 'Uploaded file is too large'):
        super().__init__(msg)
