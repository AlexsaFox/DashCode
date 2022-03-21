from flask import Blueprint, render_template, redirect, url_for
from .auth import authorization_required

index_bp = Blueprint('index', __name__)


@index_bp.get('/')
def index_view():
    return render_template('index.html')


@index_bp.get('/api-token')
@authorization_required
def api_token_view(context):
    return render_template('get_api_token.html', **context)

@index_bp.post('/api-token')
@authorization_required
def regenerate_api_token(context):
    context['user'].regenerate_api_token()
    return redirect(url_for('webapp.index.api_token_view'))
