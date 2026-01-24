from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from catalog.models import Catalog
from users.models import Reader


# Create your models here.
class Borrowed(models.Model):
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    book = models.ForeignKey(Catalog, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.reader} borrowed {self.book} on {self.borrow_date.date()}"

    #todo check if book is overdue


class Review(models.Model):
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    book = models.ForeignKey(Catalog, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reader} rated {self.book} - {self.rating}/5"