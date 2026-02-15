# import phonenumbers
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class PhoneNumberValidator:
    def __init__(self,length):
        self.length = length
    def __call__(self, value):
        if not value.startswith('08') :
            raise ValidationError('Phone number must start with 08')
        if len(value) != self.length:
            raise ValidationError(f'Phone number must be of length {self.length} digits!!')

        if not value.isdigit():
            raise ValidationError('Phone nuber can only contain digits!!')

@deconstructible
class EmailValidator:
    def __init__(self,allowed_domains=None):
        if allowed_domains is None:
            self.allowed_domains = ['abv.bg','gmail.com','yahoo.com']
        else:
            self.allowed_domains = allowed_domains
    def __call__(self, value):
        domain = value.split('@')[-1].lower()
        if domain not in self.allowed_domains:
            raise ValidationError(f'Email address must be in {' | '.join(self.allowed_domains)}!!')


# @deconstructible
# class InternationalPhoneNumberValidator:
#     def __init__(self,default_region='BG'):
#         self.default_region = default_region
#
#     def __call__(self, value):
#         try:
#             parsed = phonenumbers.parse(value, None)
#
#             if not phonenumbers.is_valid_number(parsed):
#                 raise ValidationError('Invalid phone number')
#         except phonenumbers.NumberParseException:
#             raise ValidationError('Invalid phone number format')