from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=12)
    email = models.EmailField()
    # borrowed_book = models.ManyToManyField(Catalog, blank=True)
    # borrowing_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    subscription = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"