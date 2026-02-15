from django.urls import path

from users import views


urlpatterns = [
    path('<int:book_id>/', views.register, name='register'),
]