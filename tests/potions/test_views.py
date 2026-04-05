from django.test import TestCase
from django.urls import reverse
from model_bakery import baker

from potions.models import Potion, SecretPotions


class CreatePotionViewTest(TestCase):
    def setUp(self):
        self.user = baker.make('users.User')
        self.url = reverse('create_potion')

    def test_unauthenticated_redirects_expect_failure(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_authenticated_get_returns_200_expect_success(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'potions/create-potions.html')

    def test_valid_recipe_creates_potion_expect_success(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, {
            'herb': 'mint',
            'liquid': 'water',
            'item': 'crystal',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['result'], 'success')
        self.assertEqual(response.context['potion_name'], 'Potion of Healing')
        self.assertTrue(Potion.objects.filter(magician=self.user, name='Potion of Healing').exists())

    def test_duplicate_recipe_returns_already_learned_expect_failure(self):
        baker.make(Potion, magician=self.user, name='Potion of Healing')
        self.client.force_login(self.user)
        response = self.client.post(self.url, {
            'herb': 'mint',
            'liquid': 'water',
            'item': 'crystal',
        })
        self.assertEqual(response.context['result'], 'already_learned')
        self.assertEqual(Potion.objects.filter(magician=self.user, name='Potion of Healing').count(), 1)

    def test_invalid_recipe_returns_fail_expect_success(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, {
            'herb': 'mint',
            'liquid': 'milk',
            'item': 'crystal',
        })
        self.assertEqual(response.context['result'], 'fail')
        self.assertFalse(Potion.objects.filter(magician=self.user).exists())


class SecretPotionsViewTest(TestCase):
    def setUp(self):
        SecretPotions.objects.all().delete()

    def test_get_returns_200_expect_success(self):
        response = self.client.get(reverse('secret_potions'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'potions/potions-details.html')

    def test_context_contains_potions_expect_success(self):
        baker.make(SecretPotions, _quantity=3)
        response = self.client.get(reverse('secret_potions'))
        self.assertEqual(len(response.context['potions']), 3)
