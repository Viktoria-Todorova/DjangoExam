from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from catalog.models import Catalog


# Create your views here.
def home(request: HttpRequest)->HttpResponse:
    context = {
        'books': Catalog.objects.all(),
    }

    return render(request, 'catalog/home.html', context)

def search_books(request):
    title = request.GET.get('title', '')
    writer = request.GET.get('writer', '')

    books = Catalog.objects.all()
    if title:
        books = books.filter(title__icontains=title)
    if writer:
        books = books.filter(writer__icontains=writer)

    context = {
        'books': books,
    }

    return render(request, 'catalog/search_result.html',context)

def all_books(request: HttpRequest) -> HttpResponse:
    books = Catalog.objects.all()
    context = {
        'books': books,
    }

    return render(request, 'catalog/all_books.html', context)
