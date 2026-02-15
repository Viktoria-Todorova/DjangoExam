from django.urls import path

from catalog.views import search_books, all_books

urlpatterns = [
    path('',search_books,name='home'),
    path('all_books/',all_books,name='all_books'),
]
