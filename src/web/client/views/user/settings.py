from functools import wraps
from flask import Blueprint, render_template, request, url_for, redirect, flash, session

from config import active_configuration
from client.forms import flash_errors, AccountSettingsForm, UserSettingsForm
from client.views.auth import authorization_required


settings_bp = Blueprint('settings', __name__)


def allowed_file(filename: str) -> bool:
    if '.' not in filename:
        return False

    extension = filename.split['.'][-1]
    return extension in active_configuration.ALLOWED_UPLOAD_EXTENSIONS


def add_forms_to_context(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        request.environ['user_settings_form'] = UserSettingsForm()
        request.environ['account_settings_form'] = AccountSettingsForm()
        return func(*args, **kwargs)
    return wrapper


@settings_bp.get('/')
@authorization_required
@add_forms_to_context
def settings_view():
    print(request.environ.get('kek'))
    user = request.environ['user']

    account_settings_form = request.environ['account_settings_form']
    account_settings_form.email.data = user.email

    user_settings_form = request.environ['user_settings_form']
    user_settings_form.username.data = user.username
    user_settings_form.profile_color.data = user.profile_color

    return render_template('user_pages/settings.html')


@settings_bp.post('/account')
@authorization_required
@add_forms_to_context
def account_settings_handle():
    form  = request.environ['account_settings_form']
    if not form.validate():
        flash_errors(form)
        return render_template('user_pages/settings.html')

    if not request.environ['user'].check_password(form.data.get('current_password')):
        flash('Password is not correct, email/password changes were not applied')
        return render_template('user_pages/settings.html')
    
    request.environ['user'].update_info(
        email=form.email.data,
        password=form.password.data,
    )

    return redirect(url_for('webapp.user.settings.settings_view'))


@settings_bp.post('/user')
@authorization_required
@add_forms_to_context
def user_settings_handle():
    form  = request.environ['user_settings_form']
    if not form.validate():
        flash_errors(form)
        return render_template('user_pages/settings.html')

    request.environ['user'].update_info(
        username=form.username.data,
        profile_color=form.profile_color.data,
        profile_picture=form.profile_picture.data,
    )

    # If username was updated, we need to update session
    # so user doesn't get kicked out
    if form.username.data:
        session['username'] = request.environ['user'].username

    return redirect(url_for('webapp.user.settings.settings_view'))
    