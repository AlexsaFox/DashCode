from functools import wraps
from flask import Blueprint, request

from models import User


api_bp = Blueprint('api', __name__, url_prefix='/api')


def api_token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token is None:
            return ...

        return func(*args, **kwargs)
    return wrapper