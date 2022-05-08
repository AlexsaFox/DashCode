import re

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
