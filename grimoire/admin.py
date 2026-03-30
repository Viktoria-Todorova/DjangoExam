from django.contrib import admin

from grimoire.models import Grimoire


# Register your models here.

@admin.register(Grimoire)
class GrimoireAdmin(admin.ModelAdmin):
    list_display = ['magician','body','image']