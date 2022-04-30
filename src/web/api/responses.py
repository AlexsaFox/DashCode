from enum import Enum
from typing import Any
from http.client import UNAUTHORIZED


def success(data: dict[str, Any], details: str = ''):
    return {
        'data': data,
        'details': details,
        'success': True 
    }

def error(details: str = '', data: dict[str, Any] | None = None):
    return {
        'data': data or {},
        'details': details,
        'success': False
    }
