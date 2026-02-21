from django.urls import path, include

from catalog.views import SearchBooksView, AllBooksView, BookEditView, BookDetailView, BookDeleteView, HomePageView

# app_name = 'catalog'
urlpatterns = [
    path('',HomePageView.as_view(),name='home'),
    path('all_books/',AllBooksView.as_view(),name='all_books'),
    path('search_books/',SearchBooksView.as_view(),name='search_books'),
    path('<int:pk>/',include([
        path('',BookDetailView.as_view(),name='book_detail'),
        path('edit/',BookEditView.as_view(),name='book_edit'),
        path('delete/',BookDeleteView.as_view(),name='book_delete'),
    ])),
]
