# import phonenumbers
import re

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


@deconstructible
class UsernameValidator:
    regex = r'^[A-Za-z0-9_]+$'
    invalid_message = "Oops! Your username can only use letters, numbers, and underscores — no sneaky symbols allowed."


    def __call__(self, value):
        if not re.match(self.regex, value):
            raise ValidationError(self.invalid_message)