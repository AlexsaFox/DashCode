from functools import wraps
from flask import Blueprint, redirect, render_template, url_for, flash, session, request
from client.forms import RegistrationForm, LoginForm, flash_errors
from sqlalchemy.exc import IntegrityError

from models import User, db_add


auth_bp = Blueprint('auth', __name__)


def authorization_required(func):
    """ If user is not logged in, redirects them to login page """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.environ['user'] is None:
            return redirect(url_for('webapp.auth.login_view'))

        return func(*args, **kwargs)
    return wrapper


@auth_bp.get('/register')
def register_view():
    request.environ['form'] = RegistrationForm()
    return render_template('auth/register.html')


@auth_bp.post('/register')
def register_handle():
    request.environ['form'] = form = RegistrationForm()
    if not form.validate():
        flash_errors(form)
        return render_template('auth/register.html')

    try:
        user = User(
            username=form.data['username'],
            email=form.data['email'],
            password=form.data['password']
        )
        db_add(user)
    except IntegrityError:
        flash('This user already exists')
        return render_template('auth/register.html')

    session['username'] = user.username
    return redirect(url_for('webapp.index.index_view'))


@auth_bp.get('/login')
def login_view():
    request.environ['form'] = LoginForm()
    return render_template('auth/login.html')


@auth_bp.post('/login')
def login_handle():
    request.environ['form'] = form = LoginForm()
    if not form.validate():
        flash_errors(form)
        return render_template('auth/login.html')

    user: User = (
        User.query.filter_by(username=form.data['username_or_email']).first() or 
        User.query.filter_by(email=form.data['username_or_email']).first()
    )
    if user is None or not user.check_password(form.data['password']):
        flash('No user found with provided credentials')
        return render_template('auth/login.html', form=form)

    session['username'] = user.username
    return redirect(url_for('webapp.index.index_view'))


@auth_bp.get('/logout')
def logout_handle():
    session.clear()
    return redirect(url_for('webapp.index.index_view'))
