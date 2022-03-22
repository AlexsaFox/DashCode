from flask import Blueprint, render_template

index_bp = Blueprint('index', __name__)


@index_bp.get('/')
def index_view():
    return render_template('index.html')
