from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from catalog.models import Catalog
from users.forms import UserForm


# Create your views here.
def register(request: HttpRequest,book_id) -> HttpResponse:
    book = get_object_or_404(Catalog, id=book_id)
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserForm()

    return render(request, 'users/register-page.html', {"form": form,"book": book})