from django.test import TestCase
from model_bakery import baker

from dragons.models import Dragon


class DragonModelTest(TestCase):
    def test_str_returns_dragon_name_expect_success(self):
        dragon = baker.make(Dragon, name='Smaug')
        self.assertEqual(str(dragon), 'Smaug')

    def test_rider_is_null_by_default_expect_success(self):
        dragon = baker.make(Dragon, rider=None)
        self.assertIsNone(dragon.rider)

    def test_dragon_assigned_to_rider_expect_success(self):
        user = baker.make('users.User')
        dragon = baker.make(Dragon, rider=user)
        self.assertEqual(dragon.rider, user)

    def test_one_user_one_dragon_constraint_expect_failure(self):
        user = baker.make('users.User')
        baker.make(Dragon, rider=user)
        dragon2 = baker.prepare(Dragon, rider=user)
        with self.assertRaises(Exception):
            dragon2.save()
