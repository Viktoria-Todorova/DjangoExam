from django.test import TestCase

from catalog.forms import SearchForm, GenreFilterForm, BooksForm
from catalog.models import Catalog


class SearchFormTest(TestCase):
    def test_empty_search_is_valid_expect_success(self):
        form = SearchForm(data={'book_name': ''})
        self.assertTrue(form.is_valid())

    def test_search_with_text_is_valid_expect_success(self):
        form = SearchForm(data={'book_name': 'Dune'})
        self.assertTrue(form.is_valid())


class GenreFilterFormTest(TestCase):
    def test_empty_genre_is_valid_expect_success(self):
        form = GenreFilterForm(data={'genre': ''})
        self.assertTrue(form.is_valid())

    def test_valid_genre_choice_expect_success(self):
        form = GenreFilterForm(data={'genre': 'FANTASY'})
        self.assertTrue(form.is_valid())

    def test_invalid_genre_choice_expect_failure(self):
        form = GenreFilterForm(data={'genre': 'INVALID_GENRE'})
        self.assertFalse(form.is_valid())


class BooksFormTest(TestCase):
    def get_valid_data(self):
        return {
            'title': 'Dune',
            'writer': 'Frank Herbert',
            'genre': 'FANTASY',
            'quantity': 3,
        }

    def test_valid_form_expect_success(self):
        form = BooksForm(data=self.get_valid_data())
        self.assertTrue(form.is_valid(), form.errors)

    def test_missing_title_expect_failure(self):
        data = self.get_valid_data()
        data['title'] = ''
        form = BooksForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_missing_writer_expect_failure(self):
        data = self.get_valid_data()
        data['writer'] = ''
        form = BooksForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('writer', form.errors)

    def test_quantity_defaults_to_one_expect_success(self):
        data = self.get_valid_data()
        del data['quantity']
        form = BooksForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)
