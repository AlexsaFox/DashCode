import re

from src.types import ExpectedError


EMAIL_REGEXP = re.compile(r'(?=.{1,120}$)[^@]+@[^@]+\.[^@]+')
USERNAME_REGEXP = re.compile(r'[a-zA-Z0-9_\-\.]{1,80}')
PASSWORD_REGEXP = re.compile(r'.{8,}')


class ModelFieldValidationError(ExpectedError):
    def __init__(self, fields: list[str]):
        self.fields = fields
        super().__init__(
            f'validation for following fields has failed: {", ".join(fields)}'
        )
