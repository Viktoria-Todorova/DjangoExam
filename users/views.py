from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView

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


class ProfileView(LoginRequiredMixin, UpdateView):
    model = UserModel
    form_class = ProfileEditForm
    template_name = 'users/profile-page.html'
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