from django.urls import path, include

from circulation import views



urlpatterns = [
    path('<int:book_id>/', include([
        path('', views.validate_rent_a_book, name='validate_rent_a_book'),
        path('rent/',views.rent_a_book, name='rent_a_book'),
    ])),
]