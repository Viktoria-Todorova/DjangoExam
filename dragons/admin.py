from django.contrib import admin

from dragons.models import Dragon


# Register your models here.
@admin.register(Dragon)
class DragonAdmin(admin.ModelAdmin):
    list_display = ['name','photo','description','rider']