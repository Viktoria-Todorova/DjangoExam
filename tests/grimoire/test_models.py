from io import BytesIO

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from model_bakery import baker

from grimoire.models import Grimoire
from grimoire.validators import FileSizeValidator


class GrimoireModelTest(TestCase):
    def test_default_type_is_other_expect_success(self):
        user = baker.make('users.User')
        grimoire = baker.make(Grimoire, magician=user, _fill_optional=False)
        self.assertEqual(grimoire.type_of_story, Grimoire.StoryTypeChoices.OTHER)

    def test_image_is_optional_expect_success(self):
        user = baker.make('users.User')
        grimoire = baker.make(Grimoire, magician=user, image=None)
        self.assertFalse(bool(grimoire.image))

    def test_grimoire_linked_to_magician_expect_success(self):
        user = baker.make('users.User')
        grimoire = baker.make(Grimoire, magician=user)
        self.assertEqual(grimoire.magician, user)


class FileSizeValidatorTest(TestCase):
    def _make_file(self, size_bytes):
        return SimpleUploadedFile('test.jpg', b'x' * size_bytes, content_type='image/jpeg')

    def test_file_within_limit_expect_success(self):
        validator = FileSizeValidator(5)
        small_file = self._make_file(1 * 1024 * 1024)  # 1 MB
        try:
            validator(small_file)
        except ValidationError:
            self.fail('Valid file size raised ValidationError')

    def test_file_exceeds_limit_expect_failure(self):
        validator = FileSizeValidator(5)
        large_file = self._make_file(6 * 1024 * 1024)  # 6 MB
        with self.assertRaises(ValidationError) as ctx:
            validator(large_file)
        self.assertIn('5MB', str(ctx.exception))

    def test_custom_message_expect_success(self):
        validator = FileSizeValidator(2, message='Too big!')
        large_file = self._make_file(3 * 1024 * 1024)
        with self.assertRaises(ValidationError) as ctx:
            validator(large_file)
        self.assertIn('Too big!', str(ctx.exception))
