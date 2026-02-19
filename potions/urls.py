from django.urls import path

from potions.views import create_potion

urlpatterns = [
    path('',create_potion,name='create_potion'),
]