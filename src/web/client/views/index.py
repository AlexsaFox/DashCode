from flask import Blueprint, render_template, session
from .auth import authorization_required

index_bp = Blueprint('index', __name__, '/')


@index_bp.get('/')
def index_view():
    return render_template('index.html')


@index_bp.get('/secret')
@authorization_required
def secret_view(context):
    return render_template('secret.html')
