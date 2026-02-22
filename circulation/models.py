
from django.db import models

from catalog.models import Catalog
from users.models import User


class Borrowed(models.Model):
    magician = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Catalog, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.magician} borrowed {self.book} on {self.borrow_date.date()}"

    #todo check if book is overdue
