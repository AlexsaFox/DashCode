from flask import Blueprint, render_template, request

from models import User
from client.views.auth import authorization_required


profile_bp = Blueprint('profile', __name__)


@profile_bp.get('/<username>')
@authorization_required
def profile_view(username):
    owner = User.query.filter_by(username=username).first()
    if owner is None:
        request.environ['error_msg'] = f"User {username} doesn't exist :("
        return render_template('errors/404.html'), 404

    request.environ['owner'] = owner
    return render_template('user_pages/profile.html')
