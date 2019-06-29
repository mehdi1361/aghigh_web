import re
from cerberus import Validator


class BaseValidator(Validator):

    @staticmethod
    def _validate_type_datetime_str(value):
        pattern = "\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[1-2]\d|3[0-1])T(?:[0-1]\d|2[0-3]):[0-5]\d"
        pattern = re.compile(pattern)
        if pattern.match(value):
            return True
