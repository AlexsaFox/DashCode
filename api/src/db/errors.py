import re

from sqlalchemy.exc import IntegrityError


class ObjectExistsError(ValueError):
    _INTEGRITY_ERROR_REGEXP = re.compile(
        r'.* duplicate key value violates unique constraint \"(.*)\"\n'
        r'DETAIL:  Key \((.*)\)=\((.*)\) already exists\.'
    )

    def __init__(self, error: IntegrityError, object_name: str = 'entry'):
        err_msg = str(error.orig)
        group = ObjectExistsError._INTEGRITY_ERROR_REGEXP.findall(err_msg)[0]
        self.field: str = group[1]
        self.value: str = group[2]
        super().__init__(f'{object_name} with {self.field} {self.value} already exists')
