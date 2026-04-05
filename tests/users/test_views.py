import json
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from model_bakery import baker


class RegisterViewTest(TestCase):
    def get_valid_data(self):
        return {
            'username': 'newmagician',
            'password': 'StrongPass1!',
            'first_name': 'New',
            'last_name': 'Magician',
            'email': 'new@gmail.com',
            'phone_number': '',
        }

    def test_get_renders_form_expect_success(self):
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register-page.html')

    def test_post_valid_creates_user_and_redirects_expect_success(self):
        response = self.client.post(reverse('users:register'), data=self.get_valid_data())
        self.assertRedirects(response, reverse('home'))

    def test_post_valid_logs_user_in_expect_success(self):
        self.client.post(reverse('users:register'), data=self.get_valid_data())
        response = self.client.get(reverse('home'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_post_weak_password_expect_failure(self):
        data = self.get_valid_data()
        data['password'] = 'weak'
        response = self.client.post(reverse('users:register'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_post_duplicate_username_expect_failure(self):
        baker.make('users.User', username='newmagician')
        response = self.client.post(reverse('users:register'), data=self.get_valid_data())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'already exists')


class CustomLoginViewTest(TestCase):
    def setUp(self):
        self.user = baker.make('users.User', username='magician')
        self.user.set_password('StrongPass1!')
        self.user.save()

    def test_get_renders_login_form_expect_success(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login-page.html')

    def test_post_valid_credentials_expect_success(self):
        response = self.client.post(reverse('users:login'), {
            'username': 'magician',
            'password': 'StrongPass1!',
        })
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_post_invalid_credentials_expect_failure(self):
        response = self.client.post(reverse('users:login'), {
            'username': 'magician',
            'password': 'wrongpassword',
        })
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_already_authenticated_user_redirected_expect_success(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('users:login'))
        self.assertNotEqual(response.status_code, 200)


class ProfileViewTest(TestCase):
    def setUp(self):
        self.user = baker.make('users.User')
        self.url = reverse('users:profile')

    def test_unauthenticated_redirects_expect_failure(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"{reverse('users:login')}?next={self.url}")

    @patch('users.views.aggregate_profile_stats.delay')
    def test_authenticated_returns_200_expect_success(self, mock_task):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile-page.html')

    @patch('users.views.aggregate_profile_stats.delay')
    def test_context_contains_required_keys_expect_success(self, mock_task):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        for key in ['currently_rented', 'returned_books', 'potions']:
            self.assertIn(key, response.context)


class ProfileEditViewTest(TestCase):
    def setUp(self):
        self.user = baker.make('users.User')
        self.user.set_password('OldPass1!')
        self.user.save()
        self.url = reverse('users:edit-profile')

    def test_unauthenticated_redirects_expect_failure(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"{reverse('users:login')}?next={self.url}")

    def test_get_renders_form_expect_success(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/edit-profile.html')

    def test_post_valid_data_updates_profile_expect_success(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@gmail.com',
            'password': '',
            'confirm_password': '',
        })
        self.assertRedirects(response, reverse('users:profile'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')

    def test_post_with_new_password_updates_password_expect_success(self):
        self.client.force_login(self.user)
        self.client.post(self.url, {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@gmail.com',
            'password': 'NewStrongPass1!',
            'confirm_password': 'NewStrongPass1!',
        })
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewStrongPass1!'))

    def test_post_mismatched_passwords_expect_failure(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@gmail.com',
            'password': 'NewStrongPass1!',
            'confirm_password': 'DifferentPass1!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.user.check_password('NewStrongPass1!'))


class CheckUsernameViewTest(TestCase):
    def setUp(self):
        self.url = reverse('users:check-username')

    def test_existing_username_returns_taken_true_expect_success(self):
        baker.make('users.User', username='takenname')
        response = self.client.get(self.url, {'username': 'takenname'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['taken'])

    def test_available_username_returns_taken_false_expect_success(self):
        response = self.client.get(self.url, {'username': 'availablename'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['taken'])

    def test_empty_username_returns_taken_false_expect_success(self):
        response = self.client.get(self.url, {'username': ''})
        data = json.loads(response.content)
        self.assertFalse(data['taken'])
