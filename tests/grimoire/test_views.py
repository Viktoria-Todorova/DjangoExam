from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from model_bakery import baker

from grimoire.models import Grimoire


class GrimoireListViewTest(TestCase):
    def test_get_returns_200_expect_success(self):
        response = self.client.get(reverse('grimoire_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'grimoire/grimoire_list.html')

    def test_grimoires_ordered_by_newest_first_expect_success(self):
        user = baker.make('users.User')
        baker.make(Grimoire, magician=user, _quantity=3)
        response = self.client.get(reverse('grimoire_list'))
        grimoires = list(response.context['grimoires'])
        dates = [g.created_at for g in grimoires]
        self.assertEqual(dates, sorted(dates, reverse=True))


class GrimoireDetailViewTest(TestCase):
    def test_get_returns_200_expect_success(self):
        user = baker.make('users.User')
        grimoire = baker.make(Grimoire, magician=user)
        response = self.client.get(reverse('grimoire-detail', kwargs={'pk': grimoire.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'grimoire/grimoire_detail.html')

    def test_nonexistent_grimoire_returns_404_expect_failure(self):
        response = self.client.get(reverse('grimoire-detail', kwargs={'pk': 99999}))
        self.assertEqual(response.status_code, 404)


class GrimoireCreateViewTest(TestCase):
    def setUp(self):
        self.user = baker.make('users.User')
        self.url = reverse('grimoire-create')

    def test_unauthenticated_redirects_expect_failure(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_authenticated_get_returns_200_expect_success(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    @patch('grimoire.views.process_grimoire_image.delay')
    def test_post_valid_creates_grimoire_expect_success(self, mock_task):
        self.client.force_login(self.user)
        self.client.post(self.url, {
            'body': 'A tale of dragons and fire.',
            'type_of_story': 'SPELL',
        })
        self.assertTrue(Grimoire.objects.filter(magician=self.user).exists())

    @patch('grimoire.views.process_grimoire_image.delay')
    def test_post_sets_magician_to_current_user_expect_success(self, mock_task):
        self.client.force_login(self.user)
        self.client.post(self.url, {
            'body': 'A tale of dragons and fire.',
            'type_of_story': 'SPELL',
        })
        grimoire = Grimoire.objects.get(magician=self.user)
        self.assertEqual(grimoire.magician, self.user)


class GrimoireEditViewTest(TestCase):
    def setUp(self):
        self.owner = baker.make('users.User')
        self.other_user = baker.make('users.User')
        self.grimoire = baker.make(Grimoire, magician=self.owner)
        self.url = reverse('grimoire-edit', kwargs={'pk': self.grimoire.pk})

    def test_unauthenticated_redirects_expect_failure(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_owner_can_access_edit_expect_success(self):
        self.client.force_login(self.owner)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_non_owner_gets_403_expect_failure(self):
        self.client.force_login(self.other_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    @patch('grimoire.views.process_grimoire_image.delay')
    def test_owner_can_update_body_expect_success(self, mock_task):
        self.client.force_login(self.owner)
        self.client.post(self.url, {
            'body': 'Updated body text.',
            'type_of_story': 'LEGEND',
        })
        self.grimoire.refresh_from_db()
        self.assertEqual(self.grimoire.body, 'Updated body text.')

    def test_staff_can_edit_other_users_grimoire_expect_success(self):
        staff_user = baker.make('users.User', is_staff=True)
        self.client.force_login(staff_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class GrimoireDeleteViewTest(TestCase):
    def setUp(self):
        self.owner = baker.make('users.User')
        self.other_user = baker.make('users.User')
        self.grimoire = baker.make(Grimoire, magician=self.owner)
        self.url = reverse('grimoire-delete', kwargs={'pk': self.grimoire.pk})

    def test_unauthenticated_redirects_expect_failure(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_non_owner_gets_403_expect_failure(self):
        self.client.force_login(self.other_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_owner_can_delete_grimoire_expect_success(self):
        self.client.force_login(self.owner)
        self.client.post(self.url)
        self.assertFalse(Grimoire.objects.filter(pk=self.grimoire.pk).exists())

    def test_staff_can_delete_others_grimoire_expect_success(self):
        staff_user = baker.make('users.User', is_staff=True)
        self.client.force_login(staff_user)
        self.client.post(self.url)
        self.assertFalse(Grimoire.objects.filter(pk=self.grimoire.pk).exists())
