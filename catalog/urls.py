from django.urls import path

from catalog.views import home, search_books, all_books

urlpatterns = [
    path('',home,name='home'),
    path('search/', search_books, name='search_books'),
    path('all_books/',all_books,name='all_books'),
]
