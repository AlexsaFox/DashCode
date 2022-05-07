import re
from typing import Any

from src.types import ExpectedError


EMAIL_REGEXP = re.compile(r'(?=.{1,120}$)[^@]+@[^@]+\.[^@]+')
USERNAME_REGEXP = re.compile(r'[a-zA-Z0-9_\-\.]{1,80}')
PASSWORD_REGEXP = re.compile(r'.{8,}')


class ValidationError(ExpectedError):
    def __init__(self, field: str, value: Any):
        self.field = field
        self.value = value
        super().__init__(
            f'validation for field {field} has failed: invalid value "{value}"'
        )
