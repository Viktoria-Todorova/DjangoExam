from django.test import TestCase
from django.urls import reverse
from model_bakery import baker

from dragons.models import Dragon
from potions.models import Potion


class DisplayDragonViewTest(TestCase):
    def test_get_returns_200_expect_success(self):
        response = self.client.get(reverse('display-dragons'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dragons/display-page.html')

    def test_context_contains_dragons_expect_success(self):
        baker.make(Dragon, _quantity=3)
        response = self.client.get(reverse('display-dragons'))
        self.assertEqual(response.context['dragons'].count(), 3)


class RandomDragonViewTest(TestCase):
    def setUp(self):
        self.user = baker.make('users.User')
        self.url = reverse('random-dragon')
        Dragon.objects.all().delete()

    def test_unauthenticated_redirects_expect_failure(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_user_already_has_dragon_shows_it_expect_success(self):
        dragon = baker.make(Dragon, rider=self.user, photo='https://example.com/dragon.jpg')
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['dragon'], dragon)
        self.assertFalse(response.context['newly_matched'])

    def test_not_enough_potions_cannot_match_expect_failure(self):
        self.client.force_login(self.user)
        baker.make(Potion, magician=self.user, name='Only One Potion')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['can_match'])

    def test_enough_potions_assigns_dragon_expect_success(self):
        baker.make(Dragon, rider=None, photo='https://example.com/dragon.jpg')
        baker.make(Potion, magician=self.user, name='Potion of Healing')
        baker.make(Potion, magician=self.user, name='Potion of Clarity')
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['can_match'])
        self.user.refresh_from_db()
        self.assertTrue(Dragon.objects.filter(rider=self.user).exists())

    def test_enough_potions_no_available_dragons_expect_failure(self):
        other_user = baker.make('users.User')
        baker.make(Dragon, rider=other_user, photo='https://example.com/dragon.jpg')
        baker.make(Potion, magician=self.user, name='Potion of Healing')
        baker.make(Potion, magician=self.user, name='Potion of Clarity')
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context['dragon'])
