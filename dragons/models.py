from django.db import models

from users.models import User


# Create your models here.

class Dragon(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField()
    description = models.TextField()
    rider = models.OneToOneField(User,on_delete=models.CASCADE,default=None)

    def __str__(self):
        return self.name
