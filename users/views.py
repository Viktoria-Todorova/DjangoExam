
from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView

from circulation.models import Borrowed
from dragons.models import Dragon
from potions.models import Potion
from users.forms import UserForm, ProfileEditForm

# Create your views here.

# def create_user(request: HttpRequest) -> HttpResponse:
#     if request.method == "POST":
#         form = UserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = UserForm()
#
#     return render(request, 'users/register-page.html', {"form": form})
#
#




UserModel = get_user_model()


class RegisterView(CreateView):
    model = UserModel
    form_class = UserForm
    template_name = 'users/register-page.html'
    success_url = reverse_lazy('home')  # todo to login page

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        self.object = user
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())


class CustomLoginView(LoginView):
    template_name = 'users/login-page.html'
    redirect_authenticated_user = True


from django.core.paginator import Paginator

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        borrowed = Borrowed.objects.filter(magician=user)
        
        # Pagination for Currently Rented
        currently_rented_list = borrowed.filter(return_date__isnull=True).order_by('-due_date')
        rented_paginator = Paginator(currently_rented_list, 3) # 3 per page
        rented_page = self.request.GET.get('rented_page')
        context['currently_rented'] = rented_paginator.get_page(rented_page)

        # Pagination for History
        history_list = borrowed.filter(return_date__isnull=False).order_by('-return_date')
        history_paginator = Paginator(history_list, 3)
        history_page = self.request.GET.get('history_page')
        context['returned_books'] = history_paginator.get_page(history_page)

        # Pagination for Potions
        potions_list = Potion.objects.filter(magician=user).order_by('-created_on')
        potions_paginator = Paginator(potions_list, 2)
        potions_page = self.request.GET.get('potions_page')
        context['potions'] = potions_paginator.get_page(potions_page)

        context['dragon'] = Dragon.objects.filter(rider=user).first()
        context['now'] = timezone.now()
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = UserModel
    form_class = ProfileEditForm
    template_name = 'users/edit-profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        if password:
            user.set_password(password)
        user.save()
        messages.success(self.request, '✨ Your profile has been updated successfully!')
        return HttpResponseRedirect(self.get_success_url())

class CheckUsernameView(View):
    def get(self, request):
        username = request.GET.get('username', '')
        taken = UserModel.objects.filter(username=username).exists()
        return JsonResponse({'taken': taken})