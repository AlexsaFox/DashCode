from flask import request
from functools import wraps
from http.client import UNAUTHORIZED

from models import User, API_TOKEN_ERROR
from .responses import error

def api_token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header is None or ' ' not in auth_header:
            return error('Authorization header is invalid or missing'), UNAUTHORIZED

        auth_type, token = auth_header.split(' ')
        if auth_type != 'Bearer':
            return error('only "Bearer" authorization type is supported')

        user_or_error = User.from_api_token(token)
        match user_or_error:
            case API_TOKEN_ERROR.VALIDATION_ERROR:
                return error('token validation error'), UNAUTHORIZED

            case API_TOKEN_ERROR.EXPIRED:
                return error('token expired'), UNAUTHORIZED

            case API_TOKEN_ERROR.BAD_STRUCTURE:
                return error('"key" or "exp" fields in token are missing'), UNAUTHORIZED

            case API_TOKEN_ERROR.NOT_FOUND:
                return error('user not found'), UNAUTHORIZED

            case User():
                request.environ['user'] = user_or_error
                return func(*args, **kwargs)

    return wrapper