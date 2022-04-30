from flask import Blueprint, send_from_directory

from config import active_configuration

uploads_bp = Blueprint('uploads', __name__)


@uploads_bp.route('<filename>')
def download_file(filename):
    return send_from_directory(active_configuration.UPLOAD_FOLDER, filename)
