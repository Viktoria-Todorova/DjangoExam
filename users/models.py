from django.db import models

from users.validators import EmailValidator, PhoneNumberValidator


# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(validators=[PhoneNumberValidator(10)])
    email = models.EmailField(validators=[EmailValidator()])

    def __str__(self):
        return f"{self.first_name} {self.last_name}"