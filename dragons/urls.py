from django.urls import path

from dragons.views import display_dragons, random_dragon

urlpatterns =[
    path('',display_dragons, name='display-dragons'),
    path('random/',random_dragon,name='random-dragon'),
]