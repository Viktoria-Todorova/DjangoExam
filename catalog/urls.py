from django.urls import path

from catalog.views import SearchBooksView, AllBooksView

urlpatterns = [
    path('',SearchBooksView.as_view(),name='home'),
    path('all_books/',AllBooksView.as_view(),name='all_books'),
]
