from django.db import models

from grimoire.validators import FileSizeValidator
from users.models import User


# Create your models here.

class Grimoire(models.Model):
    class StoryTypeChoices(models.TextChoices):
        SPELL = "SPELL", "Spell"
        POTION = "POTION", "Potion Recipe"
        PROPHECY = "PROPHECY", "Prophecy"
        CURSE = "CURSE", "Curse"
        LEGEND = "LEGEND", "Legend"
        MYTH = "MYTH", "Myth"
        FAIRYTALE = "FAIRYTALE", "Fairy Tale"
        RITUAL = "RITUAL", "Ritual"
        ALCHEMY = "ALCHEMY", "Alchemy Notes"
        CHRONICLE = "CHRONICLE", "Chronicle"
        DREAM = "DREAM", "Dream Vision"
        SONG = "SONG", "Magical Song"
        OTHER = "OTHER", "Other"

    body = models.TextField(blank=False, null=False,
                            )
    magician =models.ForeignKey(User, on_delete=models.CASCADE,related_name='grimoires')
    created_at = models.DateTimeField(auto_now_add=True)
    type_of_story =models.CharField(max_length=20,choices=StoryTypeChoices.choices,default=StoryTypeChoices.OTHER)
    image =models.ImageField(upload_to="grimoire_images/",blank=True,null=True,
                             validators=[FileSizeValidator(5)])