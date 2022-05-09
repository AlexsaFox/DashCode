from typing import Any


def check_auth(data: dict[str, Any] | None, errors: list[dict[str, Any]] | None):
    assert data is None
    assert errors is not None
    assert errors[0]['message'] == 'Authentication required'
