
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from users.forms import UserForm



# Create your views here.

def create_user(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserForm()

    return render(request, 'users/register-page.html', {"form": form})




