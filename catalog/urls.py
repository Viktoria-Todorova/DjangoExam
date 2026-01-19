from django.urls import path

from catalog.views import home, search_books

urlpatterns = [
    path('',home),
    path('search/', search_books, name='search_books'),
]
