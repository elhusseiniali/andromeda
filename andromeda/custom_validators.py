from flask_validator import Validator
from phonenumbers import carrier, parse
from phonenumbers.phonenumberutil import number_type


class ValidatePhoneNumber(Validator):
    def __init__(self, field, allow_null=True, throw_exception=False,
                 message=None):
        Validator.__init__(self, field, allow_null, throw_exception, message)

    def check_value(self, value):
        # NOTE: the phone number must be a valid international number
        return carrier._is_mobile(number_type(parse(value)))
