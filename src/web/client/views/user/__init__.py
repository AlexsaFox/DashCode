from flask import Blueprint

from .settings import settings_bp
from .profile import profile_bp

user_web_bp = Blueprint('user', __name__)
user_web_bp.register_blueprint(settings_bp, url_prefix='/settings')
user_web_bp.register_blueprint(profile_bp, url_prefix='/p')
