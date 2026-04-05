from django.test import TestCase

from grimoire.forms import GrimoireForm
from grimoire.models import Grimoire


class GrimoireFormTest(TestCase):
    def get_valid_data(self):
        return {
            'body': 'This is a magical story about dragons and potions.',
            'type_of_story': Grimoire.StoryTypeChoices.SPELL,
        }

    def test_valid_form_without_image_expect_success(self):
        form = GrimoireForm(data=self.get_valid_data())
        self.assertTrue(form.is_valid(), form.errors)

    def test_missing_body_expect_failure(self):
        data = self.get_valid_data()
        data['body'] = ''
        form = GrimoireForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('body', form.errors)

    def test_type_of_story_required_expect_failure(self):
        form = GrimoireForm(data={'body': 'Some text', 'type_of_story': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('type_of_story', form.errors)

    def test_invalid_type_of_story_expect_failure(self):
        data = self.get_valid_data()
        data['type_of_story'] = 'INVALID_TYPE'
        form = GrimoireForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('type_of_story', form.errors)
