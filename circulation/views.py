from datetime import timedelta
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from catalog.models import Catalog
from circulation.forms import LoginForm
from circulation.models import Borrowed
from users.models import User


# Create your views here.

def validate_rent_a_book(request: HttpRequest,book_id) -> HttpResponse:
    book = get_object_or_404(Catalog,id=book_id)
    return render(request, 'circulation/rent.html', {'book':book})


def rent_a_book(request: HttpRequest,book_id) -> HttpResponse:
    book = get_object_or_404(Catalog,id=book_id)
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            magician_username = form.cleaned_data['magician']
            try:
                user = User.objects.get(username=magician_username)
            except User.DoesNotExist:
                form.add_error('magician', "No user with this username exists!")
                return render(request, 'circulation/log-page.html', {"form": form, "book": book})
            Borrowed.objects.create(magician=user, book=book, due_date=timezone.now() + timedelta(days=25))
            book.quantity -= 1
            book.save()
            return redirect('home')
    else:
        form = LoginForm()

    return render(request, 'circulation/log-page.html', {"form": form, "book": book})

