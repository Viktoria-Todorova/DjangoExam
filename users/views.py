from datetime import timedelta

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from catalog.models import Catalog
from circulation.models import Borrowed
from users.forms import UserForm


# Create your views here.
def register(request: HttpRequest,book_id) -> HttpResponse:
    book = get_object_or_404(Catalog, id=book_id)
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()  #getting the created user from here so i can match him later with the borrowed book
            Borrowed.objects.create(reader=user, book=book, due_date=timezone.now() + timedelta(days=25))
            book.quantity -=1
            book.save()
            return redirect('home')
    else:
        form = UserForm()

    return render(request, 'users/register-page.html', {"form": form,"book": book})