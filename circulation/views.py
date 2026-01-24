from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404

from catalog.models import Catalog


# Create your views here.

def rent_a_book(request: HttpRequest,book_id) -> HttpResponse:
    book = get_object_or_404(Catalog,id=book_id)
    return render(request, 'circulation/rent.html', {'book':book})

def register(request: HttpRequest,book_id) -> HttpResponse:
    book = get_object_or_404(Catalog,id=book_id)
    if book.quantity > 1:
        book.quantity -= 1
        book.save()

    return render(request, 'circulation/register-page.html', {'title':book.title,'book':book})

