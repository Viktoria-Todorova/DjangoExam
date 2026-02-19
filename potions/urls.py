from django.urls import path

from potions.views import CreatePotionView, SecretPotionsView

urlpatterns = [
    path('create/',CreatePotionView.as_view(),name='create_potion'),
    path('secret_potions/', SecretPotionsView.as_view(), name='secret_potions'),
]