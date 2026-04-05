from django.test import TestCase
from django.urls import reverse
from model_bakery import baker

from catalog.models import Catalog


class HomePageViewTest(TestCase):
    def test_get_returns_200_expect_success(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_context_contains_books_expect_success(self):
        baker.make(Catalog, _quantity=3)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)


class AllBooksViewTest(TestCase):
    def setUp(self):
        Catalog.objects.all().delete()

    def test_get_returns_200_expect_success(self):
        response = self.client.get(reverse('all_books'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/all_books.html')

    def test_genre_filter_returns_correct_books_expect_success(self):
        baker.make(Catalog, genre=Catalog.Genre.FANTASY, _quantity=2)
        baker.make(Catalog, genre=Catalog.Genre.HORROR, _quantity=3)
        response = self.client.get(reverse('all_books'), {'genre': 'FANTASY'})
        self.assertEqual(len(response.context['books']), 2)

    def test_no_filter_returns_all_books_expect_success(self):
        baker.make(Catalog, _quantity=5)
        response = self.client.get(reverse('all_books'))
        self.assertEqual(response.context['books'].count(), 5)


class SearchBooksViewTest(TestCase):
    def test_get_with_query_returns_matching_books_expect_success(self):
        baker.make(Catalog, title='Dune')
        baker.make(Catalog, title='Harry Potter')
        response = self.client.get(reverse('search_books'), {'book_name': 'Dune'})
        self.assertEqual(len(response.context['books']), 1)

    def test_get_empty_query_returns_no_books_expect_success(self):
        baker.make(Catalog, _quantity=3)
        response = self.client.get(reverse('search_books'), {'book_name': ''})
        self.assertEqual(len(response.context['books']), 0)

    def test_get_partial_title_returns_match_expect_success(self):
        baker.make(Catalog, title='The Dune Chronicles')
        response = self.client.get(reverse('search_books'), {'book_name': 'dune'})
        self.assertEqual(len(response.context['books']), 1)


class BookDetailViewTest(TestCase):
    def test_existing_book_returns_200_expect_success(self):
        book = baker.make(Catalog)
        response = self.client.get(reverse('book_detail', kwargs={'pk': book.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/book_detail.html')

    def test_nonexistent_book_returns_404_expect_failure(self):
        response = self.client.get(reverse('book_detail', kwargs={'pk': 99999}))
        self.assertEqual(response.status_code, 404)


class BookCreateViewTest(TestCase):
    def setUp(self):
        self.url = reverse('book_create')
        self.admin = baker.make('users.User', is_staff=True)
        self.regular_user = baker.make('users.User', is_staff=False)

    def test_unauthenticated_user_gets_403_expect_failure(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_non_admin_gets_403_expect_failure(self):
        self.client.force_login(self.regular_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_admin_can_access_expect_success(self):
        self.client.force_login(self.admin)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_admin_can_create_book_expect_success(self):
        self.client.force_login(self.admin)
        response = self.client.post(self.url, {
            'title': 'New Book',
            'writer': 'New Writer',
            'genre': 'FANTASY',
            'quantity': 1,
        })
        self.assertRedirects(response, reverse('all_books'))
        self.assertTrue(Catalog.objects.filter(title='New Book').exists())


class BookEditViewTest(TestCase):
    def setUp(self):
        self.book = baker.make(Catalog, title='Old Title')
        self.url = reverse('book_edit', kwargs={'pk': self.book.pk})
        self.admin = baker.make('users.User', is_staff=True)
        self.regular_user = baker.make('users.User', is_staff=False)

    def test_non_admin_gets_403_expect_failure(self):
        self.client.force_login(self.regular_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_admin_can_edit_book_expect_success(self):
        self.client.force_login(self.admin)
        self.client.post(self.url, {
            'title': 'Updated Title',
            'writer': self.book.writer,
            'genre': self.book.genre,
            'quantity': 1,
        })
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Title')


class BookDeleteViewTest(TestCase):
    def setUp(self):
        self.book = baker.make(Catalog)
        self.url = reverse('book_delete', kwargs={'pk': self.book.pk})
        self.admin = baker.make('users.User', is_staff=True)
        self.regular_user = baker.make('users.User', is_staff=False)

    def test_non_admin_gets_403_expect_failure(self):
        self.client.force_login(self.regular_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_admin_can_delete_book_expect_success(self):
        self.client.force_login(self.admin)
        self.client.post(self.url)
        self.assertFalse(Catalog.objects.filter(pk=self.book.pk).exists())


class CatalogSearchAPIViewTest(TestCase):
    def test_api_returns_200_expect_success(self):
        response = self.client.get(reverse('api_search_books'))
        self.assertEqual(response.status_code, 200)

    def test_api_search_by_title_returns_matches_expect_success(self):
        baker.make(Catalog, title='Dune')
        baker.make(Catalog, title='Harry Potter')
        response = self.client.get(reverse('api_search_books'), {'search': 'Dune'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)

    def test_api_search_no_match_returns_empty_expect_success(self):
        baker.make(Catalog, title='Dune')
        response = self.client.get(reverse('api_search_books'), {'search': 'zzznomatch'})
        self.assertEqual(response.data['count'], 0)
