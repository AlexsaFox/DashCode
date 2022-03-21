from flask import Blueprint

from .misc import misc_bp


api_bp = Blueprint('api', __name__)

api_bp.register_blueprint(misc_bp, url_prefix='/')
