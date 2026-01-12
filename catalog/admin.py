from django.contrib import admin

from catalog.models import Catalog


# Register your models here.
@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ['title','writer','genre']
    list_filter = ['genre']
    search_fields = ['title']