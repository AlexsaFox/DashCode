import os
from flask import Blueprint

from .auth import auth_bp
from .index import index_bp


template_dir = os.path.abspath('client/templates')

webapp_bp = Blueprint('webapp', __name__, template_folder=template_dir)
webapp_bp.register_blueprint(auth_bp, url_prefix='/auth')
webapp_bp.register_blueprint(index_bp, url_prefix='/')
