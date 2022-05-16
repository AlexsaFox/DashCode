from typing import Any, Callable, Mapping

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.config import Configuration
from src.db.errors import ObjectExistsError
from src.db.validation import ModelFieldValidationError


class ValidationMixin:
    validators: Mapping[str, Callable[[Any], bool]]

    def validate_fields(self, **kwargs: Any):
        kwargs = {f: v for f, v in kwargs.items() if v is not None}

        error_fields = []
        for field, value in kwargs.items():
            validate = self.validators.get(field)
            if validate is None:
                raise ValueError(f'Unknown field: {field}')

            if not validate(value):
                error_fields.append(field)

        if error_fields:
            raise ModelFieldValidationError(self, error_fields)

    def update_fields(self, session: Session, validate: bool = True, **kwargs: Any):
        kwargs = {f: v for f, v in kwargs.items() if v is not None}
        if validate:
            self.validate_fields(**kwargs)

        # Fields are already validated, so it's guaranteed that
        # no impostors will be among them
        for field, value in kwargs.items():
            setattr(self, field, value)

        try:
            session.add(self)
            session.commit()
        except IntegrityError as err:
            raise ObjectExistsError(err)


class AppConfigurationMixin:
    config: Configuration

    @staticmethod
    def init_config(config: Configuration):
        AppConfigurationMixin.config = config
