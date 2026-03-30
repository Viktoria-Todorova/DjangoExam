from django.contrib import admin

from potions.models import Potion


# Register your models here.
@admin.register(Potion)
class PotionAdmin(admin.ModelAdmin):
    list_display = ['name','magician','created_on']