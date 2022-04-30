from flask import Blueprint, request

from .auth import api_token_required
from .responses import success

misc_bp = Blueprint('misc', __name__, url_prefix='/')


@misc_bp.post('/health')
def health_check():
    return {'ok': True}, 200


@misc_bp.post('/whoami')
@api_token_required
def whoami():
    resp = success({
        'username': request.environ['user'].username
    })
    return resp, 200
