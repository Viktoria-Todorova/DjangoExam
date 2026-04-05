from django.test import TestCase
from django.utils import timezone
from model_bakery import baker

from circulation.models import Borrowed


class BorrowedModelTest(TestCase):
    def test_str_returns_magician_and_book_expect_success(self):
        borrowed = baker.make(Borrowed, due_date=timezone.now())
        result = str(borrowed)
        self.assertIn('borrowed', result)

    def test_return_date_is_null_by_default_expect_success(self):
        borrowed = baker.make(Borrowed, due_date=timezone.now())
        self.assertIsNone(borrowed.return_date)

    def test_borrowed_linked_to_user_expect_success(self):
        user = baker.make('users.User')
        borrowed = baker.make(Borrowed, magician=user, due_date=timezone.now())
        self.assertEqual(borrowed.magician, user)

    def test_borrowed_linked_to_book_expect_success(self):
        book = baker.make('catalog.Catalog')
        borrowed = baker.make(Borrowed, book=book, due_date=timezone.now())
        self.assertEqual(borrowed.book, book)
