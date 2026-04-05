from django.test import TestCase
from model_bakery import baker

from catalog.models import Catalog


class CatalogModelStrTest(TestCase):
    def test_str_returns_title_and_writer_expect_success(self):
        book = baker.make(Catalog, title='Dune', writer='Frank Herbert')
        self.assertEqual(str(book), 'Dune by Frank Herbert')


class CatalogModelDefaultsTest(TestCase):
    def test_default_genre_is_none_expect_success(self):
        book = baker.make(Catalog, _fill_optional=False)
        self.assertEqual(book.genre, Catalog.Genre.NONE)

    def test_default_quantity_is_one_expect_success(self):
        book = baker.make(Catalog, title='T', writer='W', genre=Catalog.Genre.FANTASY)
        self.assertEqual(book.quantity, 1)

    def test_name_of_series_optional_expect_success(self):
        book = baker.make(Catalog, name_of_series=None)
        self.assertIsNone(book.name_of_series)

    def test_genre_choices_valid_expect_success(self):
        book = baker.make(Catalog, genre=Catalog.Genre.FANTASY)
        self.assertEqual(book.genre, 'FANTASY')
