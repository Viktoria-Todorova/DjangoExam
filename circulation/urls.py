from django.urls import path

from circulation.views import rent_a_book

urlpatterns=[
    path('<int:book_id>/',rent_a_book,name='rent_a_book'),
]