from django.contrib import admin

from circulation.models import Borrowed


# Register your models here.
@admin.register(Borrowed)
class BorrowedAdmin(admin.ModelAdmin):
    list_display = ['magician','book', 'borrow_date','due_date','return_date']