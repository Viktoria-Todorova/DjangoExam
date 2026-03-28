from django.urls import path, include

from catalog.views import BookCreateView
from circulation.views import ValidateRentABookView, RentABookView

urlpatterns = [
    path('validate/<int:book_id>/', ValidateRentABookView.as_view(), name='validate_rent_a_book'),
    path('rent/<int:book_id>/', RentABookView.as_view(), name='rent_a_book'),
    path('create/',BookCreateView.as_view(), name='book_create'),
]