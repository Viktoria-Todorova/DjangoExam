from django.core.exceptions import ValidationError
from django.test import TestCase
from model_bakery import baker

from users.validators import PhoneNumberValidator


class UserModelStrTest(TestCase):
    def test_str_returns_full_name_expect_success(self):
        user = baker.make('users.User', first_name='Harry', last_name='Potter')
        self.assertEqual(str(user), 'Harry Potter')

    def test_str_with_empty_names_expect_success(self):
        user = baker.make('users.User', first_name='', last_name='')
        self.assertEqual(str(user), ' ')


class PhoneNumberValidatorTest(TestCase):
    def setUp(self):
        self.validator = PhoneNumberValidator(10)

    def test_valid_phone_number_expect_success(self):
        try:
            self.validator('0812345678')
        except ValidationError:
            self.fail('Valid phone number raised ValidationError')

    def test_phone_not_starting_with_08_expect_failure(self):
        with self.assertRaises(ValidationError) as ctx:
            self.validator('0912345678')
        self.assertIn('must start with 08', str(ctx.exception))

    def test_phone_too_short_expect_failure(self):
        with self.assertRaises(ValidationError) as ctx:
            self.validator('081234')
        self.assertIn('length 10', str(ctx.exception))

    def test_phone_too_long_expect_failure(self):
        with self.assertRaises(ValidationError) as ctx:
            self.validator('081234567890')
        self.assertIn('length 10', str(ctx.exception))

    def test_phone_with_letters_expect_failure(self):
        with self.assertRaises(ValidationError) as ctx:
            self.validator('081234567a')
        self.assertIn('only contain digits', str(ctx.exception))

    def test_phone_number_required_expect_failure(self):
        with self.assertRaises(Exception):
            baker.make('users.User', phone_number=None)
