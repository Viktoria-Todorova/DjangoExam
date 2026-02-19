from django.urls import path, include

from grimoire.views import GrimoireListView, GrimoireDetailView, GrimoireCreateView, GrimoireEditView, \
    GrimoireDeleteView

urlpatterns = [
    path('',GrimoireListView.as_view(), name='grimoire_list'),
    path('create', GrimoireCreateView.as_view(), name='grimoire-create'),
    path('<int:pk>/',include([
        path('',GrimoireDetailView.as_view(), name='grimoire-detail'),
        path('edit/',GrimoireEditView.as_view(), name='grimoire-edit'),
        path('delete/',GrimoireDeleteView.as_view(), name='grimoire-delete'),
    ]) )
]

