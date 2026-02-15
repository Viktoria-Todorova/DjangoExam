from django.urls import path

from dragons import views

urlpatterns =[
    path('',views.DisplayDragonView.as_view(), name='display-dragons'),
    path('random/',views.RandomDragonView.as_view(),name='random-dragon'),
]