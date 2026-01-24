from django.urls import path, include

from circulation import views



urlpatterns = [
    path('<int:book_id>/', include([
        path('', views.rent_a_book, name='rent_a_book'),
    ])),
]