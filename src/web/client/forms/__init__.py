from flask import flash
from flask_wtf import FlaskForm

from .auth import RegistrationForm, LoginForm
from .settings import AccountSettingsForm, UserSettingsForm


def flash_errors(form: FlaskForm):
    """ Flashes all form errors """
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'{getattr(form, field).label.text}: {error}')
