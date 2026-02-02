from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from catalog.models import Catalog


# Create your views here.
def home(request: HttpRequest)->HttpResponse:
    return render(request, 'catalog/home.html')

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
#todo i want to filter them by genre
def all_books(request: HttpRequest) -> HttpResponse:
    books = Catalog.objects.all()
    context = {
        'books': books,
    }
    return render(request, 'catalog/all_books.html', context)

#todo
def book_delete(request: HttpRequest,pk)->HttpResponse:
    #only if admin
    return render(request, 'catalog/books_delete.html', context)

def book_edit(request: HttpRequest,pk)->HttpResponse:
    #only if admin
    #add validations
    return render(request, 'catalog/books_edit.html', context)