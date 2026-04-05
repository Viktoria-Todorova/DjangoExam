from django.contrib.auth.models import AbstractUser

from django.db import models

from users.validators import PhoneNumberValidator

# Create your models here.
class User(AbstractUser):

    phone_number = models.CharField(validators=[PhoneNumberValidator(10)],unique=True)
    email = models.EmailField(unique=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"