import os
from flask import Blueprint, request, session

from models import User

from .auth import auth_bp
from .index import index_bp
from .user import user_web_bp
from .uploads import uploads_bp


template_dir = os.path.abspath('client/templates')

webapp_bp = Blueprint('webapp', __name__, template_folder=template_dir)
webapp_bp.register_blueprint(index_bp, url_prefix='/')
webapp_bp.register_blueprint(auth_bp, url_prefix='/auth')
webapp_bp.register_blueprint(user_web_bp, url_prefix='/user')
webapp_bp.register_blueprint(uploads_bp, url_prefix='/uploads')


@webapp_bp.before_request
def hook():
    username = session.get('username')
    request.environ['user'] = User.query.filter_by(username=username).first()
