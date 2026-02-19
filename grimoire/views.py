from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView

from grimoire.forms import GrimoireForm, DeleteGrimoireForm
from grimoire.models import Grimoire
from users.models import User


# Create your views here.

class GrimoireCreateView(CreateView):
    model = Grimoire
    form_class = GrimoireForm
    success_url = reverse_lazy('grimoire_list')

    # def form_valid(self, form):
    #     form.instance.magician = User.objects.get(pk=self.request.user.pk)
    #     return super().form_valid(form)

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



class GrimoireEditView(UpdateView):
    model = Grimoire
    form_class = GrimoireForm
    template_name = 'grimoire/grimoire_edit.html'

    success_url = reverse_lazy('grimoire_list')

class GrimoireDeleteView(DeleteView):
    model = Grimoire
    template_name = 'grimoire/grimoire_delete.html'
    success_url = reverse_lazy('grimoire_list')
    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        context['form']=DeleteGrimoireForm(instance=self.object)
        return context