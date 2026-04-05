from django.test import TestCase

from potions.forms import CreatePotionForm


class CreatePotionFormTest(TestCase):
    def test_valid_form_with_correct_choices_expect_success(self):
        form = CreatePotionForm(data={
            'herb': 'mint',
            'liquid': 'water',
            'item': 'crystal',
        })
        self.assertTrue(form.is_valid(), form.errors)

    def test_invalid_herb_choice_expect_failure(self):
        form = CreatePotionForm(data={
            'herb': 'unicorn_dust',
            'liquid': 'water',
            'item': 'crystal',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('herb', form.errors)

    def test_invalid_liquid_choice_expect_failure(self):
        form = CreatePotionForm(data={
            'herb': 'mint',
            'liquid': 'lemonade',
            'item': 'crystal',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('liquid', form.errors)

    def test_invalid_item_choice_expect_failure(self):
        form = CreatePotionForm(data={
            'herb': 'mint',
            'liquid': 'water',
            'item': 'lucky_coin',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('item', form.errors)

    def test_missing_all_fields_expect_failure(self):
        form = CreatePotionForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)
