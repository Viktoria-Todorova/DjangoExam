from django.db import models

from users.models import User


# Create your models here.

class Potion(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    magician = models.ForeignKey(User, on_delete=models.CASCADE, related_name='potions')



class SecretPotions(models.Model):
    potion=models.CharField(max_length=100)
    herb=models.CharField(max_length=100)
    liquid=models.CharField(max_length=100)
    items=models.CharField(max_length=100)
