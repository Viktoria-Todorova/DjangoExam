from django.urls import path, include

from catalog.views import BookCreateView
from circulation.views import ValidateRentABookView, RentABookView, RulesView, ReturnBookView

urlpatterns = [
    path('rules/<int:book_id>/', RulesView.as_view(), name='rent_rules'),
    path('validate/<int:book_id>/', ValidateRentABookView.as_view(), name='validate_rent_a_book'),
    path('rent/<int:book_id>/', RentABookView.as_view(), name='rent_a_book'),
    path('return/<int:borrowed_id>/', ReturnBookView.as_view(), name='return_book'),
    path('create/', BookCreateView.as_view(), name='book_create'),
]