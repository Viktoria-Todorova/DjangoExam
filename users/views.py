from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404

from catalog.models import Catalog


# Create your views here.
def register(request: HttpRequest,book_id) -> HttpResponse:
    book = get_object_or_404(Catalog,id=book_id)
    if book.quantity > 1:
        book.quantity -= 1
        book.save()

    return render(request, 'users/register-page.html', {'title':book.title,'book':book})