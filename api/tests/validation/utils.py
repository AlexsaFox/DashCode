from typing import Any


def check_validation_error(validation_error: dict[str, Any], err_fields: list[str]):
    assert validation_error['__typename'] == 'ValidationError'

    # Check that all error fields are present in error
    returned_err_fields = {
        field_data['field']: field_data['details']
        for field_data in validation_error['fields']
    }
    for field in err_fields:
        assert field in returned_err_fields.keys()
        assert returned_err_fields[field] is not None

    # Check that no extra fields are present
    assert len(validation_error['fields']) == len(err_fields)
