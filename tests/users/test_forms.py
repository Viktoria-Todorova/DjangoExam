from django.test import TestCase
from model_bakery import baker

from users.forms import UserForm, ProfileEditForm


class UserFormTest(TestCase):
    def get_valid_data(self):
        return {
            'username': 'testmagician',
            'password': 'StrongPass1!',
            'first_name': 'Test',
            'last_name': 'Magician',
            'email': 'test@gmail.com',
            'phone_number': '0812345678',
        }

    def test_valid_form_expect_success(self):
        form = UserForm(data=self.get_valid_data())
        self.assertTrue(form.is_valid(), form.errors)

    def test_missing_username_expect_failure(self):
        data = self.get_valid_data()
        data['username'] = ''
        form = UserForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_weak_password_no_uppercase_expect_failure(self):
        data = self.get_valid_data()
        data['password'] = 'weakpass1!'
        form = UserForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)

    def test_weak_password_too_short_expect_failure(self):
        data = self.get_valid_data()
        data['password'] = 'Ab1!'
        form = UserForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)

    def test_phone_number_optional_expect_success(self):
        data = self.get_valid_data()
        data['phone_number'] = ''
        form = UserForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_duplicate_email_expect_failure(self):
        baker.make('users.User', email='test@gmail.com')
        form = UserForm(data=self.get_valid_data())
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)


class ProfileEditFormTest(TestCase):
    def get_valid_data(self):
        return {
            'first_name': 'Updated',
            'last_name': 'Magician',
            'email': 'updated@gmail.com',
            'password': '',
            'confirm_password': '',
        }

    def test_valid_form_without_password_expect_success(self):
        form = ProfileEditForm(data=self.get_valid_data())
        self.assertTrue(form.is_valid(), form.errors)

    def test_valid_form_with_matching_passwords_expect_success(self):
        data = self.get_valid_data()
        data['password'] = 'NewStrongPass1!'
        data['confirm_password'] = 'NewStrongPass1!'
        form = ProfileEditForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_passwords_do_not_match_expect_failure(self):
        data = self.get_valid_data()
        data['password'] = 'NewStrongPass1!'
        data['confirm_password'] = 'DifferentPass1!'
        form = ProfileEditForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)

    def test_weak_new_password_expect_failure(self):
        data = self.get_valid_data()
        data['password'] = 'weak'
        data['confirm_password'] = 'weak'
        form = ProfileEditForm(data=data)
        self.assertFalse(form.is_valid())

    def test_duplicate_email_other_user_expect_failure(self):
        baker.make('users.User', email='updated@gmail.com')
        form = ProfileEditForm(data=self.get_valid_data())
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_same_email_current_user_expect_success(self):
        user = baker.make('users.User', email='updated@gmail.com')
        form = ProfileEditForm(data=self.get_valid_data(), instance=user)
        self.assertTrue(form.is_valid(), form.errors)



class UserFormTest(TestCase):
    def get_valid_data(self):
        return {
            'username': 'testmagician',
            'password': 'StrongPass1!',
            'first_name': 'Test',
            'last_name': 'Magician',
            'email': 'test@gmail.com',
            'phone_number': '0812345678',
        }

    def test_valid_form_expect_success(self):
        form = UserForm(data=self.get_valid_data())
        self.assertTrue(form.is_valid(), form.errors)

    def test_missing_username_expect_failure(self):
        data = self.get_valid_data()
        data['username'] = ''
        form = UserForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_weak_password_no_uppercase_expect_failure(self):
        data = self.get_valid_data()
        data['password'] = 'weakpass1!'
        form = UserForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)

    def test_weak_password_too_short_expect_failure(self):
        data = self.get_valid_data()
        data['password'] = 'Ab1!'
        form = UserForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)

    def test_phone_number_optional_expect_success(self):
        data = self.get_valid_data()
        data['phone_number'] = ''
        form = UserForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)


class ProfileEditFormTest(TestCase):
    def get_valid_data(self):
        return {
            'first_name': 'Updated',
            'last_name': 'Magician',
            'email': 'updated@gmail.com',
            'password': '',
            'confirm_password': '',
        }

    def test_valid_form_without_password_expect_success(self):
        form = ProfileEditForm(data=self.get_valid_data())
        self.assertTrue(form.is_valid(), form.errors)

    def test_valid_form_with_matching_passwords_expect_success(self):
        data = self.get_valid_data()
        data['password'] = 'NewStrongPass1!'
        data['confirm_password'] = 'NewStrongPass1!'
        form = ProfileEditForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_passwords_do_not_match_expect_failure(self):
        data = self.get_valid_data()
        data['password'] = 'NewStrongPass1!'
        data['confirm_password'] = 'DifferentPass1!'
        form = ProfileEditForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)

    def test_weak_new_password_expect_failure(self):
        data = self.get_valid_data()
        data['password'] = 'weak'
        data['confirm_password'] = 'weak'
        form = ProfileEditForm(data=data)
        self.assertFalse(form.is_valid())
