from django.test import TestCase
from model_bakery import baker

from potions.models import Potion, SecretPotions


class PotionModelTest(TestCase):
    def test_potion_linked_to_magician_expect_success(self):
        user = baker.make('users.User')
        potion = baker.make(Potion, magician=user)
        self.assertEqual(potion.magician, user)

    def test_potion_name_and_description_stored_expect_success(self):
        user = baker.make('users.User')
        potion = baker.make(Potion, name='Potion of Healing', description='Heals wounds', magician=user)
        self.assertEqual(potion.name, 'Potion of Healing')
        self.assertEqual(potion.description, 'Heals wounds')

    def test_user_can_have_multiple_potions_expect_success(self):
        user = baker.make('users.User')
        baker.make(Potion, magician=user, _quantity=3)
        self.assertEqual(Potion.objects.filter(magician=user).count(), 3)


class SecretPotionsModelTest(TestCase):
    def test_secret_potion_stores_ingredients_expect_success(self):
        sp = baker.make(SecretPotions, potion='Healing', herb='mint', liquid='water', items='crystal')
        self.assertEqual(sp.herb, 'mint')
        self.assertEqual(sp.liquid, 'water')
        self.assertEqual(sp.items, 'crystal')
