from flask import Blueprint

from ..auth import authorization_required


profile_bp = Blueprint('profile', __name__)


@profile_bp.get('/<username>')
@authorization_required
def profile_view(username):
    return f'You are {username}', 200
