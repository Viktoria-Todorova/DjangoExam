from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView

from grimoire.forms import GrimoireForm, DeleteGrimoireForm
from grimoire.models import Grimoire



# Create your views here.

from django.core.exceptions import PermissionDenied

class GrimoireCreateView(LoginRequiredMixin, CreateView):
    model = Grimoire
    form_class = GrimoireForm
    success_url = reverse_lazy('grimoire_list')

    def form_valid(self, form):
        form.instance.magician = self.request.user
        return super().form_valid(form)

class GrimoireListView(ListView):
    model = Grimoire
    template_name = 'grimoire/grimoire_list.html'
    context_object_name = 'grimoires'
    ordering = ['-created_at']
    paginate_by = 3

class GrimoireDetailView(DetailView):
    model = Grimoire
    template_name = 'grimoire/grimoire_detail.html'
    context_object_name = 'grimoire'


class GrimoireEditView(LoginRequiredMixin, UpdateView):
    model = Grimoire
    form_class = GrimoireForm
    template_name = 'grimoire/grimoire_edit.html'
    success_url = reverse_lazy('grimoire_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.magician != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("You are not the owner of this grimoire entry!")
        return obj


class GrimoireDeleteView(LoginRequiredMixin, DeleteView):
    model = Grimoire
    template_name = 'grimoire/grimoire_delete.html'
    success_url = reverse_lazy('grimoire_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.magician != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("You are not the owner of this grimoire entry!")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DeleteGrimoireForm(instance=self.object)
        return context