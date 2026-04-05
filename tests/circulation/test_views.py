from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from model_bakery import baker

from catalog.models import Catalog
from circulation.models import Borrowed


class RulesViewTest(TestCase):
    def setUp(self):
        self.book = baker.make(Catalog)
        self.url = reverse('rent_rules', kwargs={'book_id': self.book.pk})
        self.user = baker.make('users.User')

    def test_unauthenticated_redirects_expect_failure(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_authenticated_returns_200_expect_success(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'circulation/log-page.html')


class ValidateRentABookViewTest(TestCase):
    def setUp(self):
        self.book = baker.make(Catalog)
        self.url = reverse('validate_rent_a_book', kwargs={'book_id': self.book.pk})
        self.user = baker.make('users.User')

    def test_unauthenticated_redirects_expect_failure(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_authenticated_returns_200_expect_success(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'circulation/rent.html')


class RentABookViewTest(TestCase):
    def setUp(self):
        self.user = baker.make('users.User')
        self.book = baker.make(Catalog, quantity=3)
        self.url = reverse('rent_a_book', kwargs={'book_id': self.book.pk})

    def test_unauthenticated_redirects_expect_failure(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)

    @patch('circulation.views.process_book_rental.delay')
    def test_post_logged_in_redirects_to_home_expect_success(self, mock_task):
        self.client.force_login(self.user)
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('home'))
        mock_task.assert_called_once_with(self.user.id, self.book.pk)

    @patch('circulation.views.process_book_rental.delay')
    def test_post_nonexistent_book_returns_404_expect_failure(self, mock_task):
        self.client.force_login(self.user)
        response = self.client.post(reverse('rent_a_book', kwargs={'book_id': 99999}))
        self.assertEqual(response.status_code, 404)


class ReturnBookViewTest(TestCase):
    def setUp(self):
        self.user = baker.make('users.User')
        self.book = baker.make(Catalog)
        self.borrowed = baker.make(
            Borrowed,
            magician=self.user,
            book=self.book,
            due_date=timezone.now(),
            return_date=None,
        )
        self.url = reverse('return_book', kwargs={'borrowed_id': self.borrowed.pk})

    def test_unauthenticated_redirects_expect_failure(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)

    @patch('circulation.views.process_book_return.delay')
    def test_post_logged_in_redirects_to_profile_expect_success(self, mock_task):
        self.client.force_login(self.user)
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('users:profile'))
        mock_task.assert_called_once_with(self.borrowed.pk)

    @patch('circulation.views.process_book_return.delay')
    def test_post_wrong_user_returns_404_expect_failure(self, mock_task):
        other_user = baker.make('users.User')
        self.client.force_login(other_user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)
